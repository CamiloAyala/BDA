from bson import ObjectId
from src.cli_terminal import TerminalInterface
from dotenv import dotenv_values
from pymongo import MongoClient, InsertOne
from pymongo.errors import BulkWriteError

class ETL:
    '''
        This class will be used to orchestrate the ETL process.
    '''
    def __init__(self) -> None:
        '''
            Initializes the ETL class, which will be used to orchestrate the ETL process.
        '''
        self._env = dotenv_values('.env')
        self._extractor = MongoClient(f'mongodb://{self._env["URL_HOST"]}:50001/')['bda_oltp']
        self._loader = MongoClient(f'mongodb://{self._env["URL_HOST"]}:50002/')['bda_olap']
        self._interface = TerminalInterface()

    def _find(self, collection_name:str, *, filter:str = {}, projection:str = {}, search_in_ldap:bool = False) -> list:
        '''
            Extracts the data from the collection with the given name in the OLTP database.

            @param {str} collection_name - The name of the collection from which the data will be extracted.
            @returns {list} - A list with the documents extracted from the collection.
        '''
        db = self._loader if search_in_ldap else self._extractor
        data = []

        for document in db[collection_name].find(filter, projection):
            data.append(document)

        return data
    
    def _aggregate(self, collection_name:str, pipeline:list) -> list:
        '''
            Extracts the data from the collection with the given name in the OLTP database.

            @param {str} collection_name - The name of the collection from which the data will be extracted.
            @returns {list} - A list with the documents extracted from the collection.
        '''
        data = []

        for document in self._extractor[collection_name].aggregate(pipeline):
            data.append(document)

        return data

    def _insertMany(self, collection_name:str, data:list) -> None:
        '''
            Loads the data into the collection with the given name in the data warehouse.

            @param {str} collection_name - The name of the collection into which the data will be loaded.
            @param {list} data - A list with the documents to be loaded into the collection.
        '''
        bulk = []

        for document in data:
            bulk.append(InsertOne(document))

        try:
            self._loader[collection_name].bulk_write(bulk, ordered=False)
        except BulkWriteError as e:
            pass

    def _operateStudents(self) -> None:
        '''
            Orchestrates the ETL process for the students.
        '''
        # Extracting data
        self._interface.print('Extracting data for the students dimension')
        programs = self._find('programs', projection={"subjects": 0})
        progrmas_ids = [program['_id'] for program in programs]
        students = self._find('students', projection={"programs.semesters": 0})

        for student in students:
            for program in student['programs']:
                if program['id'] in progrmas_ids:
                    program['name'] = programs[progrmas_ids.index(program['id'])]['name']
                    break

        # Loading data
        self._interface.print('Loading data into the students dimension')
        self._insertMany('student_dim', students)

        # Ending process
        self._interface.print('Data loaded into the students dimension', static=True)

    def _operateTeachers(self) -> None:
        '''
            Orchestrates the ETL process for the teachers.
        '''
        # Extracting data
        self._interface.print('Extracting data for the teachers dimension')
        data = self._find('teachers')

        # Loading data
        self._interface.print('Loading data into the teachers dimension')
        self._insertMany('teacher_dim', data)

        # Ending process
        self._interface.print('Data loaded into the teachers dimension', static=True)

    def _operateSubjects(self) -> None:
        '''
            Orchestrates the ETL process for the subjects.
        '''
        # Extracting data
        self._interface.print('Extracting data for the subjects dimension')
        subjects = self._find('subjects')
        subjects_ids = [subject['_id'] for subject in subjects]
        programs = self._find('programs')
        campuses = self._find('campus')

        subjects_faculties = {}

        for campus in campuses:
            for faculty in campus['faculties']:
                for program in faculty['programs']:
                    if program not in subjects_faculties:
                        subjects_faculties[program] = faculty['name']

        for program in programs:
            for subject in program['subjects']:
                if subject in subjects_ids:
                    if not 'programs' in subjects[subjects_ids.index(subject)]:
                        subjects[subjects_ids.index(subject)]['programs'] = []
                        
                    subjects[subjects_ids.index(subject)]['programs'].append({'_id': program['_id'], 'name': program['name'], 'faculty': subjects_faculties[program['_id']]})

        # Loading data
        self._interface.print('Loading data into the subjects dimension')
        self._insertMany('subject_dim', subjects)

        # Ending process
        self._interface.print('Data loaded into the subjects dimension', static=True)

    def _operateClassrooms(self) -> None:
        '''
            Orchestrates the ETL process for the classrooms.
        '''
        # Extracting data
        self._interface.print('Extracting data for the classrooms dimension')
        campuses = self._find('campus')
        classrooms = self._find('classrooms')
        classrooms_ids = [classroom['_id'] for classroom in classrooms]

        for campus in campuses:
            for faculty in campus['faculties']:
                for classroom in faculty['classrooms']:
                    if classroom in classrooms_ids:
                        if not 'faculties' in classrooms[classrooms_ids.index(classroom)]:
                            classrooms[classrooms_ids.index(classroom)]['faculties'] = []

                        if not 'campuses' in classrooms[classrooms_ids.index(classroom)]:
                            classrooms[classrooms_ids.index(classroom)]['campuses'] = []

                        faculty_dict = {'name': faculty['name']}
                        campus_dict = {'_id': campus['_id'], 'name': campus['name']}

                        if faculty_dict  not in classrooms[classrooms_ids.index(classroom)]['faculties']:classrooms[classrooms_ids.index(classroom)]['faculties'].append({'name': faculty['name']})
                        if campus_dict not in classrooms[classrooms_ids.index(classroom)]['campuses']:classrooms[classrooms_ids.index(classroom)]['campuses'].append({'_id': campus['_id'], 'name': campus['name']})

        # Loading data
        self._interface.print('Loading data into the classrooms dimension')
        self._insertMany('classroom_dim', classrooms)

        # Ending process
        self._interface.print('Data loaded into the classrooms dimension', static=True)

    def _operateTime(self) -> None:
        '''
            Orchestrates the ETL process for the time dimension.
        '''
        # Extracting data
        self._interface.print('Extracting data for the time dimension')

        times_query = self._find('enrollments', projection={'date': 1})
        times = []
        dates = set()

        for time in times_query:
            if time['date'] in dates:
                continue

            dates.add(time['date'])

            times.append({'_id': ObjectId(),'full': time['date'], 'year': time['date'].year, 'semester': 1 if time['date'].month < 7 else 2})

        # Loading data
        self._interface.print('Loading data into the time dimension')
        self._insertMany('time_dim', times)
        
        # Ending process
        self._interface.print('Data loaded into the time dimension', static=True)

    def _operateEnrolledIn(self) -> None:
        '''
            Orchestrates the ETL process for the enrolled in fact table.
        '''
        # Extracting data
        enrollments = self._find('enrollments')
        times = self._find('time_dim', projection={'_id': 1, 'full': 1},search_in_ldap=True)
            
        times_dict = {time['full'].strftime('%Y-%m-%d'): time['_id'] for time in times}


        for enrollment in enrollments:
            enrollment['time'] = times_dict[enrollment['date'].strftime('%Y-%m-%d')]
            del enrollment['date']

        students = self._find('students')
        operated_students = {}

        for student in students:
            for program in student['programs']:
                for semester in program['semesters']:
                    for enrollment in semester['enrollments']:
                        if not enrollment['enrollment'] in operated_students:
                            operated_students[enrollment['enrollment']] = [{'id': student['_id'], 'grade': enrollment['grade']}]
                        else:
                            operated_students[enrollment['enrollment']].append({'id': student['_id'], 'grade': enrollment['grade']})

        final_enrollments = []
        
        for enrollment in enrollments:
            if enrollment['_id'] in operated_students:
                for student in operated_students[enrollment['_id']]:
                    final_enrollments.append({'_id': ObjectId(), 'student': student['id'], 'subject': enrollment['subject'], 'teachers': enrollment['teachers'], 'classrooms': enrollment['classrooms'], 'time': enrollment['time']})

        enrollments = final_enrollments

        # Loading data
        self._interface.print('Loading data into the enrolled in fact table')
        self._insertMany('enrolled_in_fact', enrollments)

        # Ending process
        self._interface.print('Data loaded into the enrolled in fact table', static=True)

    def _operateGrades(self) -> None:
        '''
            Orchestrates the ETL process for the grades fact table.
        '''
        # Extracting data
        enrollments = self._find('enrollments')
        times = self._find('time_dim', projection={'_id': 1, 'full': 1},search_in_ldap=True)
            
        times_dict = {time['full'].strftime('%Y-%m-%d'): time['_id'] for time in times}


        for enrollment in enrollments:
            enrollment['time'] = times_dict[enrollment['date'].strftime('%Y-%m-%d')]
            del enrollment['date']

        students = self._find('students')
        operated_students = {}

        for student in students:
            for program in student['programs']:
                for semester in program['semesters']:
                    for enrollment in semester['enrollments']:
                        if not enrollment['enrollment'] in operated_students:
                            operated_students[enrollment['enrollment']] = [{'id': student['_id'], 'grade': enrollment['grade']}]
                        else:
                            operated_students[enrollment['enrollment']].append({'id': student['_id'], 'grade': enrollment['grade']})

        grades = []
        
        for enrollment in enrollments:
            if enrollment['_id'] in operated_students:
                for student in operated_students[enrollment['_id']]:
                    grades.append({'_id': ObjectId(), 'student': student['id'], 'subject': enrollment['subject'], 'grade': student['grade'], 'time': enrollment['time']})

        # Loading data
        self._interface.print('Loading data into the grades fact table')
        self._insertMany('grade_fact', grades)

        # Ending process
        self._interface.print('Data loaded into the grades fact table', static=True)

    def _main_menu(self) -> None:
        '''
            Displays the main menu.
        '''
        tables = ['studiantes', 'profesores', 'materias', 'salones', 'tiempos', 'inscritos', 'notas']
        options = ['Procesar todo'] + [f'Procesar {table}' for table in tables] + ['Salir']

        while True:
            option = self._interface.generateMenu('Bienvenido a la interfaz de ETL.\nA continuación seleccione una opción:', options, returnable = False, print_static=True)

            if option == 0:
                self._operateStudents()
                self._operateTeachers()
                self._operateSubjects()
                self._operateClassrooms()
                self._operateTime()
                self._operateEnrolledIn()
                self._operateGrades()
            elif option == 1: self._operateStudents()
            elif option == 2: self._operateTeachers()
            elif option == 3: self._operateSubjects()
            elif option == 4: self._operateClassrooms()
            elif option == 5: self._operateTime()
            elif option == 6: self._operateEnrolledIn()
            elif option == 7: self._operateGrades()
            elif option == 8: break

    def run(self) -> None:
        self._main_menu()