from pymongo import MongoClient
import mysql.connector
import time


def get_metrics():
    get_mongo_metrics()
    get_mysql_metrics()


def get_mongo_metrics():

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

    pipeline1_metrics = get_mongo_results(db, pipeline1)
    pipeline2_metrics = get_mongo_results(db, pipeline2)

    print('MongoDB - Métricas')
    print('Tiempo de ejecución promedio de la consulta 1: {} ms'.format(pipeline1_metrics))
    print('Tiempo de ejecución promedio de la consulta 2: {} ms'.format(pipeline2_metrics))

def get_mongo_results(db, pipeline, iterations=10):
    excution_time = 0.0
    for i in range(iterations):
        result = db.command('explain', { 'aggregate': 'enrolled_in_fact', 'pipeline': pipeline, 'cursor': {} }, verbosity='executionStats')
        time = result['stages'][0]['$cursor']['executionStats']['executionTimeMillis']
        excution_time += float(time)
        print(excution_time)
    
    return round(excution_time / iterations, 3)


def get_mysql_metrics():

    db = mysql.connector.connect(
        host="34.125.212.175",
        user="root",
        password="",
        database="college_db",
        port=50002
    )

    cursor = db.cursor()

    query1 = """
        SELECT `us_fname`, `us_lname`, `us_doc`, `us_doc_type`, `dt_year`, `dt_semester`, SUM(`sb_credits`) as `total_credits` 
        FROM `Enrolled_in_fact` 
        JOIN `User_dimension` ON (en_us_id = us_id) 
        JOIN `Subject_dimension` ON (en_sb_id = sb_id) 
        JOIN `Date_dimension` on (en_dt_id = dt_id) 
        WHERE us_role = 'Estudiante' 
        GROUP BY us_id, dt_year, dt_semester;
    """
    

    query2 = """
        SELECT `us_fname` , `us_lname` , `us_doc` , `us_doc_type` , AVG ( `sb_credits` ) AS `total_credits` 
        FROM `Enrolled_in_fact` 
        JOIN `User_dimension` ON ( `en_us_id` = `us_id` ) 
        JOIN `Subject_dimension` ON ( `en_sb_id` = `sb_id` ) 
        WHERE `us_role` = 'Estudiante'
        GROUP BY `us_id`;
    """

    query1_metrics = get_mysql_results(cursor, query1)
    query2_metrics = get_mysql_results(cursor, query2)

    print('MySQL - Métricas')
    print('Tiempo de ejecución promedio de la consulta 1: {} ms'.format(query1_metrics))

    print('\nMySQL - Métricas')
    print('Tiempo de ejecución promedio de la consulta 2: {} ms'.format(query2_metrics))

def get_mysql_results(cursor, query, iterations=10):
    exec_time = 0.0
    for i in range(iterations):
        start = time.time()
        cursor.execute(query)
        cursor.fetchall()
        end = time.time()
        exec_time += float(end - start)
    
    return round((exec_time / iterations) * 1000, 3)


def main():
    get_metrics()

if __name__ == "__main__":
    main()
