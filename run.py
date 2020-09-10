import mysql.connector as mysql
import sys
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
import os

db = mysql.connect(
    host = os.environ['HOST'],
    user = os.environ['USER'],
    passwd = os.environ['PASS'],
    database = os.environ['DB_SCHEMA']
)

def search_coincidences(ratio_tolerance):
	query = "SELECT * FROM `patients`  order by patient_first_name, patient_middle_name, patient_last_name asc"
	cursor = db.cursor()

	cursor.execute(query)

	records = cursor.fetchall()
	ids_already_on_coincidence = []
	with open('coindicencias.txt', 'a') as f:
	    for row_index in range(0, len(records)):
	        if records[row_index][0] not in ids_already_on_coincidence:
	            first_coincidence = True
	            row_string = ' '.join(str(records[row_index][cell_index]) for cell_index in range(0, len(records[row_index])) if cell_index > 0)
	            for next_row_index in range(row_index + 1, len(records)):
	                next_row_string = ' '.join(str(records[next_row_index][cell_index]) for cell_index in range(0, len(records[next_row_index])) if cell_index > 0)
	                ratio = fuzz.ratio(row_string, next_row_string)
	                if ratio > ratio_tolerance:
	                    if first_coincidence:
	                        f.write('id: {}\n'.format(records[row_index][0]))
	                    f.write('coindice con: {} en un ratio de {}\n'.format(records[next_row_index][0], ratio))
	                    ids_already_on_coincidence.append(records[next_row_index][0])
	                first_coincidence = False

if __name__ == "__main__":
    if 2 > len(sys.argv):
        print('No arguments')
        print('Usage example:')
        print('python run.py <ratio_tolerance>')
        print('ratio_tolerance: Number between 1 and 100')
    else:
        search_coincidences(int(sys.argv[1]))
