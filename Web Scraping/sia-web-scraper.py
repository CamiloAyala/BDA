from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

import time
import pandas as pd
import os


# Is necesary to download the WebDriver for the browser that you are going to use
# see: https://selenium-python.readthedocs.io/installation.html#drivers
PATH = "../chromedriver"
SIA_URL = "https://sia.unal.edu.co/Catalogo/facespublico/public/servicioPublico.jsf?taskflowId=task-flow-AC_CatalogoAsignaturas"

faculty_info = ""
degree_info = ""

driver = webdriver.Chrome(PATH)
   

def fill_form(faculty_num, degree_num) -> tuple[str, str]:
    """
    With the faculty and degree index in the corresponding select input
    fill the form until the part in that the page show the subjects table.
    """

    degree_category_element = driver.find_element(By.NAME, 'pt1:r1:0:soc1')
    degree_category_select = Select(degree_category_element)
    degree_category_select.select_by_index(1)
    print(degree_category_select.first_selected_option.text)

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable(((By.NAME, 'pt1:r1:0:soc9'))))
    campus_element = driver.find_element(By.NAME, 'pt1:r1:0:soc9')
    campus_select = Select(campus_element)
    campus_select.select_by_index(2)
    print(campus_select.first_selected_option.text)

    time.sleep(1.5)

    faculty_element = driver.find_element(By.NAME, 'pt1:r1:0:soc2')
    faculty_select = Select(faculty_element)
    faculty_select.select_by_index(faculty_num)
    faculty_info = faculty_select.first_selected_option.text
    print(faculty_info)

    #time.sleep(2)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(((By.NAME, 'pt1:r1:0:soc3'))))
    degree_element = driver.find_element(By.NAME, 'pt1:r1:0:soc3')
    degree_select = Select(degree_element)
    degree_select.select_by_index(degree_num)
    degree_info = degree_select.first_selected_option.text
    print(degree_info)


    time.sleep(5)

    subject_typo_element = driver.find_element(By.NAME, 'pt1:r1:0:soc4')
    subject_typo_select = Select(subject_typo_element)
    subject_typo_select.select_by_index(1)

    time.sleep(1)

    show_button = driver.find_element(By.CLASS_NAME, 'af_button_link')
    show_button.click()
    
    time.sleep(30)

    return faculty_info, degree_info

def getSubjects(faculty_info, degree_info) -> tuple[list, str, str]:

    """
    For a degree that belongs to a program, gets the subjects associated to that degree
    by iterating in the subjects table

    Then executes the saveData by passing the DataFrame with subjects info, faculty name 
    and the degree name.
    """

    subject_info = []
    subject_code = ""
    subject_name = ""
    subject_credit = ""
    subject_type = ""
    subject_is_active = 1

    print("Here are the results: ")
    subjects_rows = driver.find_elements(By.CLASS_NAME, 'af_table_data-row')
    print(len(subjects_rows))

    faculty_info = faculty_info.split(" ")
    faculty_code = faculty_info.pop(0)
    faculty_name = " ".join(faculty_info)

    degree_info = degree_info.split(" ")
    degree_code = degree_info.pop(0)
    degree_name = " ".join(degree_info)

    for row in subjects_rows:
        i = 0
        for cells in row.find_elements(By.CLASS_NAME, 'af_column_data-cell'):
            if(i == 0):
                subject_code = cells.text
            elif(i == 1):
                subject_name = cells.text.replace("\n", " ")
                if("ASIGNATURA SIN PROGRAMAR" in subject_name):
                    subject_is_active = 0
                    subject_name = subject_name.replace(" ASIGNATURA SIN PROGRAMAR", "")
                else:
                    subject_is_active = 1

            elif(i == 2):
                subject_credit = cells.text
            elif(i == 3):
                subject_type = cells.text[-2]
            i += 1

        subject_info.append({
            'sb_code': subject_code,
            'sb_name': subject_name,
            'sb_credits': subject_credit,
            'sb_type': subject_type,
            'sb_program_code': degree_code,
            'sb_program_name': degree_name,
            'sb_faculty_code': faculty_code,
            'sb_faculty_name': faculty_name,
            'sb_is_active': subject_is_active})
    
    return subject_info, faculty_name, degree_name

def saveData(subject_info, faculty_name, degree_name):
    """
    Saves the subjects data of a degree into a CSV file inside in a
    folder with the name of the faculty to which it belongs
    """

    if not os.path.exists(faculty_name): os.mkdir(faculty_name)

    data = pd.DataFrame(subject_info)
    data.to_csv(str(faculty_name)+"/"+str(degree_name).capitalize()+".csv",index=False)

def main():
    driver.get(SIA_URL)

    # Note: WebDriverWait sometimes crash

    #time.sleep(15)
    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID, 'pt1:r1:0:t1:w-titulo')))

    # TODO: Automate the fill form process for each degree 
    fac_info, deg_info = fill_form(2, 8)
    df, fac_name, deg_name = getSubjects(fac_info, deg_info)
    saveData(df, fac_name, deg_name)

    driver.quit()

if __name__ == '__main__':
    main()