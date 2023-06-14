from datetime import date
from faker import Faker
import random
import pandas as pd

def getUserProgram() -> tuple[str, str, str, str]:
    """
    Returns a random program info with the corresponding faculty info
    from the Programs.csv file
    """

    programs_info = pd.read_csv('Programs.csv')
    user_program = programs_info.sample(1)
    return str(user_program['program_code'].values[0]), str(user_program['program_name'].values[0]), str(user_program['faculty_code'].values[0]), str(user_program['faculty_name'].values[0])


def createUsers(quantity):

    """
    Returns a list of users with random data with length = quantity
    """

    fake = Faker('es_CO')
    userDocTypes = ['CC', 'CE']
    userRole = ['Estudiante', 'Profesor']
    userData = []
    doc_min = pow(10, 9)
    doc_max = pow(10, 10) - 1

    for i in range(1, quantity):

        birthday = fake.date_between(start_date='-40y', end_date='-16y')
        isOlder = date.today() - birthday
        docType = "TI" if not isOlder else random.choices(userDocTypes, [9, 1],k=1)[0]
        user_program_code, user_program_name, user_faculty_code, user_faculty_name = getUserProgram()
        user_doc_num = random.randint(doc_min, doc_max)

        userData.append({
            'us_id': i,
            'us_pass': 'password{}'.format(i),
            'us_fname': fake.first_name(),
            'us_lname': fake.last_name(),
            'us_bday': str(birthday),
            'us_doc': user_doc_num,
            'us_doc_type': docType,
            'us_username': fake.user_name(),
            'us_role': random.choices(userRole, [8, 2], k=1)[0],
            'us_program_code': user_program_code,
            'us_program_name': user_program_name,
            'us_faculty_code': user_faculty_code,
            'us_faculty_name': user_faculty_name,
            'us_created_at': fake.date_time_between(start_date='-7y', end_date='now'),
            'us_active': 1
        })
    
    return userData

def saveData(userData):

    """
    Saves the DataFrame in a csv file
    """

    data = pd.DataFrame(userData)
    data.to_csv("Users.csv",index=False)

def main():
    userQuantity = 10000
    df = createUsers(userQuantity)
    saveData(df)


if __name__ == '__main__':
    main()