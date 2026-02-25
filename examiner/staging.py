from .sql_utils import print_table, populate_vocabulary, validate_all_disapproved
from sqlite3 import Connection
from .validation import validate
import logging


logger = logging.getLogger(__name__)


def process_staging(conn: Connection):

	cursor = conn.cursor()
	cursor.execute('SELECT COUNT (*) FROM staging;')

	if cursor.fetchone()[0] == 0:
		logger.info("No entries require validation")
		return

	logger.info("There are entries that require validation")
	while True:
		valid_input = input("\nProceed? (y/n) ").lower()
		match valid_input:
			case 'y':
				break
			case 'n':
				return
			case _:
				logger.warning("Undefined input, try again...")

	print_table(conn, 'staging')
	while True:
		valid_input = input("\nValidate all? (y/n) ").lower()
		match valid_input:
			case 'y':
				populate_vocabulary(conn)
				validate_all_disapproved(conn)
				## clear json
				return
			case 'n':
				clear_approved = validate(conn)
				break
			case _:
				logger.warning("Undefined input, try again...")

	return clear_approved #, clear_disapproved



from examiner.sql_utils import init_sql
if __name__ == "__main__":

	conn = init_sql()
	# staging(conn)
	print_table(conn, 'staging')
	conn.close()
