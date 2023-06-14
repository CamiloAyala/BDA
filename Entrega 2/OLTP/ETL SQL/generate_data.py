import pandas as pd
import random
from faker import Faker
from datetime import date

def generateUsers(quantity):

    doc_min = pow(10, 7)
    doc_max = pow(10, 8) - 1
    userDocTypes = ['CC', 'CE']
    userRole = ['Estudiante', 'Profesor']

    users = []
    fake = Faker('es-CO')

    chunck = 500
    counter = 1
    for i in range(1, quantity):

        birthday = fake.date_between(start_date='-40y', end_date='-16y')
        isOlder = True if (date.today().year - birthday.year) >= 18 else False
        docType = "TI" if not isOlder else random.choices(userDocTypes, [9, 1],k=1)[0]
        user_doc_num = random.randint(doc_min, doc_max)

        user_program_code, user_program_name, user_faculty_code, user_faculty_name = userProgram()

        users.append({
            'us_id': i,
            'us_pass': 'password{}'.format(i),
            'us_fname': fake.first_name(),
            'us_lname': fake.last_name(),
            'us_bday': str(birthday),
            'us_doc': user_doc_num,
            'us_doc_type': docType,
            'us_username': "{}{}".format(fake.user_name(), random.randint(0, 20)),
            'us_role': random.choices(userRole, [8, 2], k=1)[0],
            'us_program_code': user_program_code,
            'us_program_name': user_program_name,
            'us_faculty_code': user_faculty_code,
            'us_faculty_name': user_faculty_name,
            'us_created_at': fake.date_time_between(start_date='-7y', end_date='now'),
            'us_active': 1
        })

        counter+=1
        
        if(len(users) == chunck):
            saveData(users, 'Users.csv')
            print(i)
            users.clear()
    
    return users


def userProgram() -> tuple[str, str, str, str]:
    """
        Returns a random program info with the corresponding faculty info
        from the Programs.csv file
    """

    program_dict = {
        0: {'program_id': 3, 'program_name': "Estadistica", 'faculty_id': 2, 'faculty_name': "Ciencias"},
        1: {'program_id': 9, 'program_name': "Ingenieria agricola", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        2: {'program_id': 10, 'program_name': "Ingenieria civil", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        3: {'program_id': 11, 'program_name': "Ingenieria de sistemas", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        4: {'program_id': 12, 'program_name': "Ingenieria electrica", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        5: {'program_id': 13, 'program_name': "Ingenieria electronica", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        6: {'program_id': 14, 'program_name': "Ingenieria industrial", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        7: {'program_id': 15, 'program_name': "Ingenieria mecanica", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        8: {'program_id': 16, 'program_name': "Ingenieria mecatronica", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        9: {'program_id': 17, 'program_name': "Ingenieria quimica", 'faculty_id': 1, 'faculty_name': "Ingeniería"},
        10: {'program_id': 18, 'program_name': "Fisioterapia", 'faculty_id': 3, 'faculty_name': "Medicina"},
        11: {'program_id': 19, 'program_name': "Fonoaudiologia", 'faculty_id': 3, 'faculty_name': "Medicina"},
        12: {'program_id': 20, 'program_name': "Medicina", 'faculty_id': 3, 'faculty_name': "Medicina"},
        13: {'program_id': 21, 'program_name': "Nutrición y dietetica", 'faculty_id': 3, 'faculty_name': "Medicina"},
        14: {'program_id': 22, 'program_name': "Terapia ocupacional", 'faculty_id': 3, 'faculty_name': "Medicina"}
    }

    data = program_dict[random.randint(0, 14)]
    return data['program_id'], data['program_name'], data['faculty_id'], data['faculty_name']


def generateEnrollments(quantity):
    enrollments = []

    teachers = pd.read_csv('Users.csv')
    students = pd.read_csv('Users.csv')

    teachers = teachers.loc[teachers['us_role'] == 'Profesor']
    students = students.loc[students['us_role'] == 'Estudiante']

    hours = {
        "7:00": "9:00",
        "9:00": "11:00",
        "11:00": "13:00",
        "14:00": "16:00",
        "16:00": "18:00",
        "18:00": "20:00",
        "10:00": "13:00",
        "14:00": "17:00",
    }

    chunck = 500
    counter = 1

    for i in range(1, quantity):

        student = students.sample(1)
        teacher = teachers.sample(1)

        key, value = random.choice(list(hours.items()))
        enrollments.append({
            'en_id': counter,
            'en_us_id': student['us_id'].values[0],
            'en_sb_id': random.randint(1, 832),
            'en_cr_id': random.randint(1,100),
            'en_dt_id': random.randint(1,1000),
            'en_teacher_id': teacher['us_id'].values[0],
            'en_shour': key,
            'en_fhour': value,
            'en_days': getSubjectDays(),     
        })

        counter+=1
    
        if(len(enrollments) == chunck):
            saveData(enrollments, 'EnrolledIn.csv')
            print(i)
            enrollments.clear()
        

    return enrollments

        
def getSubjectDays() -> str:
    """
    Returns a string with the days of the week represented a binary string
    """

    # Containes the combinations of days in which a subject can be offered in format L-S
    dayCombinations = [
        '101000',
        '010100',
        '001010',
        '101010',
        '011100',
        '001110',
        '100000',
        '001000',
        '000100',
        '000010',
        '111110',
        '000001',
    ]
         
    return random.choice(dayCombinations)

def generateGrades(quantity):
    """
        Generate random grades for Grades dimension
    """

    chunck = 500
    counter = 1

    grades = []
    for i in range(1, quantity):
        grades.append({
            'gr_id': i,
            'gr_score': round(random.uniform(0, 5), 2),
            'gr_sb_id': random.randint(1, 830),
            'gr_dt_id': random.randint(1, 1000),
            'gr_us_id': random.randint(1, 9999),
        })

        counter+=1
        
        if(len(grades) == chunck):
            saveData(grades, 'Grades.csv')
            print(i)
            grades.clear()
    
    return grades

def saveData(data, filename):
    """
        Saves a data from a list of dictionaries in a csv file
    """

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, mode="a", header=False)

def main():

    # users = generateUsers(10000)
    # saveData(users, 'Users.csv')

    enrollments = generateEnrollments(210000)
    saveData(enrollments, 'EnrolledIn.csv')

    grades = generateGrades(210000)
    saveData(grades, 'Grades.csv')

if __name__ == "__main__":
    main()