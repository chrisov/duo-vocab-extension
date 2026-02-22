from .validation import validate_all_approved, validate_all_disapproved, validate
from sqlite3 import Connection, Error
import logging
from daemon.sql_utils import print_table


logger = logging.getLogger(__name__)


def process_staging(conn: Connection):

	cursor = conn.cursor()
	cursor.execute('SELECT COUNT (*) FROM staging;')

	if cursor.fetchone()[0] == 0:
		logger.info("No changes require validation")
		return

	logger.info("There are changes that require validation")
	while True:
		valid_input = input("\nProceed with data validation? (y/n) ")
		if valid_input == 'n':
			return
		elif valid_input == 'y':
			break

	print_table(conn, 'staging')
	while True:
		valid_input = input("Validate all? (y/n) ")
		try:
			if valid_input == 'y':
				validate_all_approved(conn)
				validate_all_disapproved(conn)
				return
			elif valid_input == 'n':
				validate(conn)
				break
		except Error as e:
			conn.rollback()
			logger.warning(f"Transaction failed, rolled back: {str(e)}")


	# print("Checking for validation changes...")
	# if is_empty_validation(data) == True:
	# 	if input("\nProcced now? (y/n) ") == 'n':
	# 		print("Moving on")
	# 		continue



