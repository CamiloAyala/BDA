from pymongo import MongoClient

client = MongoClient('mongodb://35.202.156.192:50002')

db = client['bda_olap']

pipeline1 = [
    {
        '$lookup': {
            'from': "student_dim",
            'localField': "student",
            'foreignField': "_id",
            'as': "result",
        },
    },
    {
        '$unwind': "$result",
    },
    {
        '$lookup': {
            'from': "subject_dim",
            'localField': "subject",
            'foreignField': "_id",
            'as': "subject",
        },
    },
    {
        '$unwind': "$subject",
    },
    {
        '$lookup': {
            'from': "time_dim",
            'localField': "time",
            'foreignField': "_id",
            'as': "time",
        },
    },
    {
        '$unwind': "$time",
    },
    {
        '$group': {
            '_id': {
                'studentId': "$result",
                'year': "$time.year",
            },
            'name': {
                '$first': "$result.name",
            },
            'dt_year': {
                '$first': "$time.year",
            },
            'dt_semester': {
                '$first': "$time.semester",
            },
            'total_credits': {
                '$sum': {
                '$toInt': "$subject.credits",
                },
            },
        },
    },
]

pipeline2 = [
    {
        '$lookup': {
            'from': "student_dim",
            'localField': "student",
            'foreignField': "_id",
            'as': "student",
        },
    },
    {
        '$unwind': "$student",
    },
    {
        '$lookup': {
            'from': "subject_dim",
            'localField': "subject",
            'foreignField': "_id",
            'as': "subject",
        },
    },
    {
        '$unwind': "$subject",
    },
    {
        '$group': {
            '_id': {
                'studentId': "$student",
            },
            'name': {
                '$first': "$student.name",
            },
            'credits': {
                '$avg': {
                    '$toInt': "$subject.credits",
                },
            },
        },
    },
]

avg = 0.0
for i in range(1, 10):
    result = db.command('explain', { 'aggregate': 'enrolled_in_fact', 'pipeline': pipeline2, 'cursor': {} }, verbosity='executionStats')
    time = result['stages'][0]['$cursor']['executionStats']['executionTimeMillis']
    avg += time
    print(time)

avg = round(avg/10, 3)

print("\nMongoDB - Métricas")
print("Tiempo promedio de ejecución: " + str(avg) + " ms")
