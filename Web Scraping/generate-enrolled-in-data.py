import random
import pandas as pd

# def getUserSubject(program_name: str) -> str:
#     """
#     From a given program name of a student gets a list of subjects of that program

#     Returns a random subject code of the corresponding program
#     """
#     subject = ""

#     programs_info = pd.read_csv('Programs.csv')
#     programs = programs_info['program_name'].values

#     if program_name in programs:
#         faculty_name = programs_info.loc[programs_info['program_name'] == program_name]['faculty_name'].values[0]
#         subjects_info = pd.read_csv('{}/{}.csv'.format(faculty_name, program_name.capitalize()))
#         subjects = subjects_info['sb_code'].values
#         subject = random.choice(subjects)
    
#     return subject

def load_programs_info():
    programs_info = pd.read_csv('Programs.csv')
    programs_dict = {}
    for _, row in programs_info.iterrows():
        program_name = row['program_name']
        faculty_name = row['faculty_name']
        programs_dict[program_name] = faculty_name
    return programs_dict

def load_subjects_info(programs_dict):
    subjects_info_dict = {}
    for program_name, faculty_name in programs_dict.items():
        subjects_info = pd.read_csv('{}/{}.csv'.format(faculty_name, program_name.capitalize()))
        subjects_info_dict[program_name] = subjects_info['sb_code'].values
    return subjects_info_dict

def getUserSubject(program_name: str, programs_dict: dict, subjects_info_dict: dict) -> str:
    subject = ""
    if program_name in programs_dict:
        subjects = subjects_info_dict[program_name]
        subject = random.choice(subjects)
    return subject
    
def getTeachersId(program_name: str, teachers_info: pd.DataFrame):
    """
    From a given program name, returns a list with the teachers id
    """
    # teachers_info = teachers_info.loc[teachers_info['us_role'] == 'Profesor']
    teachers_id = teachers_info.loc[teachers_info['us_program_name'] == program_name]['us_id'].values
    return teachers_id


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


def enrolledIn(quantity, teachers_info, students_info ,programs_dict, subjects_info_dict):
    """
    Creates a enrolled in date for the students with a random subject from the program
    of the student, a random teacher from the program of the student, a random hour and
    a random combination of days of the week
    """

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

    enrolled_in = []
    chunck = 100
    counter = 1

    for i in range(1,quantity):

        student_info = students_info.sample(1)
        teachers_id = getTeachersId(student_info['us_program_name'].values[0], teachers_info)
        
        
        key, value = random.choice(list(hours.items()))
        enrolled_in.append({
            'en_id': counter,
            'en_us_id': student_info['us_id'].values[0],
            'en_sb_id': getUserSubject(student_info['us_program_name'].values[0], programs_dict, subjects_info_dict),
            'en_cr_id': random.randint(1,100),
            'en_dt_id': random.randint(1,1000),
            'en_teacher_id': random.choice(teachers_id),
            'en_shour': key,
            'en_fhour': value,
            'en_days': getSubjectDays(),     
        })

        counter+=1
    
        if(len(enrolled_in) == chunck):
            saveData(enrolled_in)
            print(i)
            enrolled_in.clear()
        

    return enrolled_in
    


def saveData(enrolled_in):
    """
    Saves a data from a list of dictionaries in a csv file
    """

    df = pd.DataFrame(enrolled_in)
    df.to_csv('EnrolledIn.csv', index=False, mode="a", header=False)


def main():
    teachers_info = pd.read_csv('Users.csv')
    students_info = pd.read_csv('Users.csv')

    teachers_info = teachers_info.loc[teachers_info['us_role'] == 'Profesor']
    students_info = students_info.loc[students_info['us_role'] == 'Estudiante']

    programs_dict = load_programs_info()
    subjects_info_dict = load_subjects_info(programs_dict)

    enrolled_in = enrolledIn(50000, teachers_info, students_info, programs_dict, subjects_info_dict)
    saveData(enrolled_in)

if __name__ == "__main__":
    main()



