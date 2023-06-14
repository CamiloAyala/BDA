'''
    The following sdcript is a simple ETL process that will extract data from some excel files, apply some transformations and load the data into the College_db Data Warehouse.
    The ETL process will be done in the following order:
        1. Extract data from the excel files
        2. Transform the data where necessary
        3. Load the data into the Data Warehouse directly
'''
from src.etl import ETL

def main():
    '''
        Main function of the script.
    '''
    try:
        etl = ETL()
        etl.run()
    except KeyboardInterrupt:
        print('Process stopped by the user.')

if __name__ == '__main__': main()