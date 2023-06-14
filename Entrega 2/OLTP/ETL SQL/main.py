'''
    The following sdcript is a simple ETL process that will extract data from some excel files, apply some transformations and load the data into the College_db Data Warehouse.
    The ETL process will be done in the following order:
        1. Extract data from the excel files
        2. Transform the data where necessary
        3. Load the data into the Data Warehouse directly
'''
import argparse
import os
import hashlib

import random
import string
import mysql.connector
import pandas as pd
from tqdm import tqdm


class UserInterface:
    def __init__(self, args:dict) -> None:
        '''
            Initializes the UserInterface class, which will be used to interact with the user and start the ETL process.
        '''
        self.etl = DataColector(args)

    def _presentation(self) -> None:
        '''
            Prints the presentation of the script.
        '''
        text = 'Bienvenido a la herramienta ETL para la carga de datos al Data Warehouse de la Universidad Nacional de Colombia.'
        divider = '-' * (len(text) + 4)

        print(f'{divider}\n- {text} -\n{divider}')

    def _clear(self) -> None:
        '''
            Clears the terminal screen.
        '''
        os.system('cls' if os.name == 'nt' else 'clear')

    def  _printMenu(self, title:str, options:list) -> None:
        '''
            Prints a menu with the given title and options.
            
            @param {str} title - The title of the menu
            @param {list} options - A list of the options to be printed
        '''
        error = False
        while True:
            if error: 
                self._clear()
                print('Opción inválida, intente de nuevo.')

            print(f'{title}')
            for i in range(len(options)):
                print(f'    {i+1}) {options[i]}')

            option = int(input('Seleccione su opción: '))

            if option < 1 or option > len(options):
                error = True
                
            return option
        
    def _loadData(self) -> None:
        '''
            Starts the ETL process.
        '''
        self.etl.load()

    def _cleanData(self) -> None:
        '''
            Cleans the data warehouse before loading the new data.
        '''
        stop = False
        seleccion = [False for i in range(6)]
        
        while not stop:
            options = [f"{'Resetear' if not seleccion[i] else 'No resetear'} tabla {self.etl.TABLES_NAMES[i]}" for i in range(6)]
            options.append('Finalizar selección')

            option = self._printMenu('Seleccione las tablas a resetear:', options)
            if option == 7: stop = True
            else: seleccion[option-1] = not seleccion[option-1]
            
            self._clear()

        self.etl.setDataReset(seleccion)

    def start(self):
        '''
            Starts the user interface.
        '''
        self._presentation()

        options = ['Cargar datos', 'Limpiar Data Warehouse', 'Salir']

        while True:
            option = self._printMenu('Seleccione una opción:', options)

            if option == 1:
                self._clear()
                self._loadData()
            elif option == 2:
                self._clear()
                self._cleanData()
            elif option == 3:
                print('Gracias por usar la herramienta!')
                return

class DataColector:
    TABLES_NAMES = ['Date_dimension', 'User_dimension', 'Subject_dimension', 'Classroom_dimension', 'Grades_fact', 'Enrolled_in_fact']

    def __init__(self, args:dict) -> None:
        '''
            Initializes the DataColector class, which will be used to extract data from the excel files and load it into the college data warehouse.
            The class will also be used to clean the data warehouse before loading the new data if required.
            
            @param {dict} args - A dictionary with the arguments passed to the script
        '''
        self.database = mysql.connector.connect(
            host=args['connection'],
            port=args['port'],
            user=args['user'],
            password=args['password'],
            database=args['database']
        )

        # The cursor will be used to execute queries to the database and the verbose variable will be used to print more information about the ETL process
        self.cursor = self.database.cursor()
        self.verbose = args['verbose']

        # Variables to store the names of the excel files and the sheets where the data is stored
        self.dates_names = [f'data/{args["date_file"]}', args['date_sheet']]
        self.users_names = [f'data/{args["user_file"]}', args['user_sheet']]
        self.subjects_names = [f'data/{args["subject_file"]}', args['subject_sheet']]
        self.classrooms_names = [f'data/{args["classroom_file"]}', args['classroom_sheet']]
        self.grades_names = [f'data/{args["grade_file"]}', args['grade_sheet']]
        self.enrollments_names = [f'data/{args["enrollment_file"]}', args['enrollment_sheet']]
        
        # This list will be used to keep track of which tables will be cleaned when importing data
        self.reset= [False for i in range(6)]

    def _restartTable(self, table_name:str) -> None:
        '''
            Clean and restart the table with the given name.
            This method will be used to clean the data warehouse before loading the new data.
            
            @param {str} table_name - The name of the table to be cleaned
        '''
        if self.verbose: print(f'Restarting table {table_name}...')
        self.cursor.execute(f'DELETE FROM {table_name}')
        self.cursor.execute(f'ALTER TABLE {table_name} AUTO_INCREMENT = 1')
        self.database.commit()

    def _resetTables(self) -> None:
        '''
            Cleans the data warehouse before loading the new data.
        '''
        if self.verbose and not all(self.reset): print('Cleaning selected tables from the database...')
        elif self.verbose: print('Cleaning all tables from the database...')

        for i in range(len(self.reset)):
            if self.reset[i]: self._restartTable(self.TABLES_NAMES[i])

    def setDataReset(self, reset:list[bool]) -> None:
        '''
            Sets the list of tables to be cleaned before importing data.
            
            @param {list} reset - A list of booleans that will be used to determine which tables will be cleaned
        '''
        if len(reset) != 6: raise Exception('The reset list must have 6 elements.')
        self.reset = reset

    def _cypherPassword(self, password:str) -> str:
        '''
            Returns the cyphered version of the given password using SHA512 and a salt of 12 characters.
            
            @param {str} password - The password to be cyphered
            @return {str} - The cyphered version of the given password
        '''
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=12)).encode('ascii')
        password = hashlib.sha512(salt + password.encode('ascii')).hexdigest().encode('ascii')

        return (salt + password).decode('ascii')

    def _loadDates(self):
        '''
            Loads the dates from the excel file into the data warehouse.
        '''
        if self.verbose: print('Reading dates from excel file...')
        dates_df = pd.read_excel(*self.dates_names)
        
        query = f'INSERT INTO {self.TABLES_NAMES[0]} (dt_full, dt_semester, dt_year) VALUES '

        if self.verbose: print('Inserting dates into the data warehouse...')
        for index, row in tqdm(dates_df.iterrows(), total=dates_df.shape[0], desc='Dates', disable=not self.verbose):
            query += f'("{row["Full"]}", "{row["Semester"]}", {row["Year"]}), '

        query = query[:-2] + ';'
        self.cursor.execute(query)
        self.database.commit()

    def _loadUsers(self):
        '''
            Loads the users from the excel file into the data warehouse.
            
            Transformations:
                - Passwords are cyphered using SHA512 and a salt of 12 characters
                - CreatedAt is transformed from ISO 8601 to MySQL datetime format
            '''
        if self.verbose: print('Reading users from excel file...')
        #users_df = pd.read_excel(*self.users_names)
        users_df = pd.read_csv('data/Users.csv')

        query = f'INSERT INTO {self.TABLES_NAMES[1]} (us_pass, us_fname, us_lname, us_bday, us_doc, us_doc_type, us_username, us_role, us_program_code, us_program_name, us_faculty_code, us_faculty_name, us_created_at, us_active) VALUES '

        # Cyphering the passwords
        users_df['us_pass'] = users_df['us_pass'].apply(self._cypherPassword)
        # Pass CreatedAt to datetime format from ISO 8601 to MySQL datetime format
        users_df['us_created_at'] = users_df['us_created_at'].apply(lambda x: x.replace('T', ' ').replace('Z', ''))

        if self.verbose: print('Inserting users into the data warehouse...')
        for index, row in tqdm(users_df.iterrows(), total=users_df.shape[0], desc='Users', disable=not self.verbose):
            query += f'("{row["us_pass"]}", "{row["us_fname"]}", "{row["us_lname"]}", "{row["us_bday"]}", "{row["us_doc"]}", "{row["us_doc_type"]}", "{row["us_username"]}", "{row["us_role"]}", {row["us_program_code"]}, "{row["us_program_name"]}", {row["us_faculty_code"]}, "{row["us_faculty_name"]}", "{row["us_created_at"]}", {row["us_active"]}), '

        query = query[:-2] + ';'
        self.cursor.execute(query)
        self.database.commit()

    def _loadSubjects(self):
        '''
            Loads the subjects from the excel file into the data warehouse.

            Transformations:
                - CreatedAt is transformed from ISO 8601 to MySQL datetime format
        '''
        if self.verbose: print('Reading subjects from excel file...')
        subjects_df = pd.read_excel(*self.subjects_names)

        query = f'INSERT INTO {self.TABLES_NAMES[2]} (sb_name, sb_credits, sb_type, sb_program_code, sb_program_name, sb_faculty_code, sb_faculty_name, sb_created_at, sb_active) VALUES '

        # Pass CreatedAt to datetime format from ISO 8601 to MySQL datetime format
        subjects_df['CreatedAt'] = subjects_df['CreatedAt'].apply(lambda x: x.replace('T', ' ').replace('Z', ''))

        if self.verbose: print('Inserting subjects into the data warehouse...')
        for index, row in tqdm(subjects_df.iterrows(), total=subjects_df.shape[0], desc='Subjects', disable=not self.verbose):
            query += f'(\'{row["Name"]}\', {row["Credits"]}, \'{row["Type"]}\', {row["ProgramCode"]}, \'{row["ProgramName"]}\', {row["FacultyCode"]}, \'{row["FacultyName"]}\', \'{row["CreatedAt"]}\', {row["Active"]}), '

        query = query[:-2] + ';'
        self.cursor.execute(query)
        self.database.commit()

    def _loadClassrooms(self):
        '''
            Loads the classrooms from the excel file into the data warehouse.
        '''
        if self.verbose: print('Reading classrooms from excel file...')
        classrooms_df = pd.read_excel(*self.classrooms_names)

        query = f'INSERT INTO {self.TABLES_NAMES[3]} (cr_number, cr_has_pcs, cr_capacity, cr_building_number, cr_building_name, cr_campus_code, cr_campus_name, cr_faculty_code, cr_faculty_name, cr_building_latitude, cr_building_longitude, cr_name) VALUES '

        if self.verbose: print('Inserting classrooms into the data warehouse...')
        for index, row in tqdm(classrooms_df.iterrows(), total=classrooms_df.shape[0], desc='Classrooms', disable=not self.verbose):
            query += f'(\'{row["Number"]}\', {row["HasPCs"]}, {row["Capacity"]}, {row["BuildingNumber"]}, \'{row["BuildingName"]}\', {row["CampusCode"]}, \'{row["CampusName"]}\', {row["FacultyCode"]}, \'{row["FacultyName"]}\', {row["Latitude"]}, {row["Longitude"]}, \'{row["Name"]}\'), '

        query = query[:-2] + ';'
        self.cursor.execute(query)
        self.database.commit()

    def _loadGrades(self):
        '''
            Loads the grades from the excel file into the data warehouse.
        '''
        if self.verbose: print('Reading grades from excel file...')
        # grades_df = pd.read_excel(*self.grades_names)
        grades_df = pd.read_csv('data/Grades.csv')
        query = f'INSERT INTO {self.TABLES_NAMES[4]} (gr_score, gr_sb_id, gr_dt_id, gr_us_id) VALUES '

        if self.verbose: print('Inserting grades into the data warehouse...')
        for index, row in tqdm(grades_df.iterrows(), total=grades_df.shape[0], desc='Grades', disable=not self.verbose):
            query += f'(\'{row["Score"]}\', {row["SubjectId"]}, {row["DateId"]}, {row["UserId"]}), '

        query = query[:-2] + ';'
        self.cursor.execute(query)
        self.database.commit()

    def _loadEnrollments(self):
        '''
            Loads the enrollments from the excel file into the data warehouse.
        '''
        if self.verbose: print('Reading enrollments from excel file...')
        #enrollments_df = pd.read_excel(*self.enrollments_names)
        enrollments_df = pd.read_csv('data/EnrolledIn.csv')

        query = f'INSERT INTO {self.TABLES_NAMES[5]} (en_us_id, en_sb_id, en_cr_id, en_dt_id, en_teacher, en_shour, en_fhour, en_days) VALUES '

        if self.verbose: print('Inserting enrollments into the data warehouse...')
        for index, row in tqdm(enrollments_df.iterrows(), total=enrollments_df.shape[0], desc='Enrollments', disable=not self.verbose):
            query += f'(\'{row["UserId"]}\', {row["SubjectId"]}, {row["ClassroomId"]}, {row["DateId"]}, \'{row["Teacher"]}\', \'{row["StartHour"]}\', \'{row["FinishHour"]}\', \'{row["Days"]}\'), '

        query = query[:-2] + ';'
        self.cursor.execute(query)
        self.database.commit()

    def load(self) -> None:
        '''
            Loads all the data from the excel files into the data warehouse.
        '''
        # self. _resetTables()

        # Stop the execution for 2 

        # self._loadDates()
        # self._loadUsers()
        # self._loadSubjects()
        # self._loadClassrooms()
        self._loadGrades()
        # self._loadEnrollments()

def parseArguments():
    '''
        Parses the arguments passed to the script.
    '''
    parser = argparse.ArgumentParser() 

    parser.add_argument('-c', '--connection', type=str, default='34.125.212.175', help='The host or ip of the connection to the database')
    parser.add_argument('-d', '--database', type=str, default='college_db', help='The name of the database where the data is stored')
    parser.add_argument('-p', '--port', type=int , default=50002, help='The port where the database engine is listening')
    parser.add_argument('-u', '--user', type=str, default='root', help='The user with reading permissions to the database')
    parser.add_argument('-pw', '--password', type=str, default='', help='The password of the user - Default is blank, make sure to change it if required')
    parser.add_argument('--date_file', type=str, default='Date.xlsx', help='The name of the excel file where the dates are stored')
    parser.add_argument('--date_sheet', type=str, default='Sheet1', help='The name of the sheet where the dates are stored')
    parser.add_argument('--user_file', type=str, default='User.xlsx', help='The name of the excel file where the users are stored')
    parser.add_argument('--user_sheet', type=str, default='Sheet1', help='The name of the sheet where the users are stored')
    parser.add_argument('--subject_file', type=str, default='Subject.xlsx', help='The name of the excel file where the subjects are stored')
    parser.add_argument('--subject_sheet', type=str, default='Sheet1', help='The name of the sheet where the subjects are stored')
    parser.add_argument('--classroom_file', type=str, default='Classroom.xlsx', help='The name of the excel file where the classrooms are stored')
    parser.add_argument('--classroom_sheet', type=str, default='Sheet1', help='The name of the sheet where the classrooms are stored')
    parser.add_argument('--grade_file', type=str, default='Grades.xlsx', help='The name of the excel file where the grades are stored')
    parser.add_argument('--grade_sheet', type=str, default='Sheet1', help='The name of the sheet where the grades are stored')
    parser.add_argument('--enrollment_file', type=str, default='Enrolled in.xlsx', help='The name of the excel file where the enrollments are stored')
    parser.add_argument('--enrollment_sheet', type=str, default='Sheet1', help='The name of the sheet where the enrollments are stored')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print more information about what is happening in the ETL logic')
    parser.set_defaults(verbose=False)

    return vars(parser.parse_args())

def main():
    '''
        Main function of the script.
    '''
    args = parseArguments()

    interface = UserInterface(args)

    interface.start()


if __name__ == '__main__': main()