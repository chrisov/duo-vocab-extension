from sqlite3 import Connection
import logging
from examiner.sql_utils import populate_vocabulary, populate_translation
from tabulate import tabulate

logger = logging.getLogger(__name__)


def validate_all_disapproved(conn: Connection):
	pass



def	validate_all_approved(conn: Connection):
	cursor = conn.cursor()

	cursor.execute('''INSERT OR IGNORE INTO vocabulary (
					Word,
					Article,
					Language,
					Plural,
					Grammar,
					Category,
					Difficulty,
					Count,
					SuccessRate)
				SELECT Word,
					Article,
					Language,
					Plural,
					Grammar,
					Category,
					Difficulty,
					Count,
					SuccessRate
				from staging;
				''')
	
	cursor.execute("DELETE * FROM staging")
	conn.commit()
	logger.info("All data approved")



def validate(conn: Connection):
	cursor = conn.cursor()
	
	## Load table
	cursor.execute("SELECT * FROM staging;")
	rows = cursor.fetchall()
	columns = [description[0] for description in cursor.description]
	
	## Count the rows
	cursor.execute("SELECT COUNT (*) FROM staging")
	count = cursor.fetchone()[0]

	for i, row in enumerate(rows, 1):

		print("\n" + tabulate([row], headers=columns, tablefmt="fancy_grid"))

		user_input = input(f"\n{i}/{count}: Approve / edit / delete / quit? (a/e/d/q) ").lower()
		while True:
			match user_input:
				case 'a':
					populate_vocabulary(conn, row[0], row[2])
					populate_translation(conn, row[0], row[2])
					cursor.execute("DELETE FROM staging WHERE Word = ? AND Language = ?", (row[0], row[2], ))
					logger.info(f"Approved: '{row[0]}' ✅")
					break;
				case 'd':
					cursor.execute("DELETE FROM staging WHERE Word = ? AND Language = ?", (row[0], row[2], ))
					logger.info(f"Deleted: '{row[0]}' 🗑️")
					break;
				case 'e':
					logger.info("Moving on")
					break;
				case 'q':
					logger.info("Quitting...")
					conn.commit()
					return
				case _:
					logger.warning("Undefined input, try again...")
	
	conn.commit()
	logger.info("All data validated")
	
