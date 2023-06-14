import pandas as pd
import os

listFaculties = ["FACULTAD DE ARTES", "FACULTAD DE CIENCIAS", "FACULTAD DE INGENIERÍA"]
data = pd.DataFrame
aux = 0
header = True
for i in range(len(listFaculties)):
    files = os.scandir(listFaculties[i]+"/")
    for f in files:
        file_info = pd.read_csv("{}/{}".format(listFaculties[i], f.name))
        data = pd.DataFrame(file_info)
        if aux > 0 : header = False
        data.to_csv('Subjects.csv', index=False, header=header, mode="a")
        aux+= 1
