from sqlite3 import Connection, Error
import logging
from examiner.sql_utils import populate_one_vocabulary, populate_one_translation, delete_one, update_query, print_row, append_to_column
from tabulate import tabulate


logger = logging.getLogger(__name__)


def edit_entry(conn: Connection, table_name: str, keys: list) -> bool:

	while True:
		user_input = input(
			"\nEdit property:\n"
			"Put '+' after the distinctive (e.g. 'g+') to append to a property\n"
			"(a: Article / e: English / p: Plural / g: Grammar / c: Category / q: Quit): "
		).lower()

		match user_input:
			case 'a':
				new_value = input("New Article: ").lower()
				update_query(conn, table_name, ['Article', new_value], keys)
			case 'a+':
				new_value = input("Append Article: ").lower()
				append_to_column(conn, table_name, ['Article', new_value], keys)
			case 'e':
				new_value = input("New English: ").lower()
				update_query(conn, table_name, ['English', new_value], keys)
			case 'e+':
				new_value = input ("Append English: ").lower()
				append_to_column(conn, table_name, ['English', new_value], keys)
			case 'p':
				new_value = input("New Plural: ").lower()
				update_query(conn, table_name, ['Plural', new_value], keys)
			case 'p+':
				new_value = input ("Append Plural: ").lower()
				append_to_column(conn, table_name, ['Plural', new_value], keys)
			case 'g':
				new_value = input("New Grammar: ").capitalize()
				update_query(conn, table_name, ['Gramamr', new_value], keys)
			case 'g+':
				new_value = input("Append Grammar: ").capitalize()
				append_to_column(conn, table_name, ['Grammar', new_value], keys)
			case 'c':
				new_value = input ("New Category: ").capitalize()
				update_query(conn, table_name, ['Category', new_value], keys)
			case 'c+':
				new_value = input ("New Category: ").capitalize()
				append_to_column(conn, table_name, ['Category', new_value], keys)
			case 'q':
				return
			case _:
				logger.warning("Undefined input, try again...")
				continue

		if input("Continue editing query (y/n)? ").lower() == 'n':
			break
	
	print_row(conn, table_name, keys)
	logger.info(f"'{table_name}': Changes overview.")

	while True:
		edit_input = input(f"\nApply changes in {keys} (y/n)? ").lower()
		match edit_input:
			case 'y':
				return True
			case 'n':
				conn.rollback()
				logger.warning(f"Changes rejected 🚫")
				return False
			case _:
				logger.warning("Undefined input, try again...")



def delete_entry(conn: Connection, keys: list):
	
	delete_one(conn, 'staging', keys, msg=True)
	
	while True:
		del_input = input(f"\nAre you sure you want to delete {keys} (y/n)? ").lower()
		match del_input:
			case 'y':
				return conn.commit()
			case 'n':
				return conn.rollback()
			case _:
				logger.warning("Undefined input, try again...")



def add_entry(conn: Connection, keys:list):
	try:
		populate_one_vocabulary(conn, keys)
		populate_one_translation(conn, keys)
		delete_one(conn, 'staging', keys)
		conn.commit()
		logger.info(f"Approved: {keys} ✅")
	except Error as e:
		conn.rollback()
		logger.error(f"Add entry: Transaction failed: {str(e)}")



def validate(conn: Connection) -> list:

	cursor = conn.cursor()
	result = []
	
	## Load table
	cursor.execute("SELECT * FROM staging;")
	rows = cursor.fetchall()
	columns = [description[0] for description in cursor.description]
	
	## Count the rows
	cursor.execute("SELECT COUNT (*) FROM staging")
	count = cursor.fetchone()[0]

	for i, row in enumerate(rows, 1):

		print("\n" + tabulate([row], headers=columns, tablefmt="fancy_grid"))

		user_input = input(f"\n{i}/{count}: Approve / edit / delete / skip / quit (a/e/d/s/q)? ").lower()
		while True:
			match user_input:
				case 'a':
					add_entry(conn, [row[0], row[2]])
					result.append(row[0])
					break
				case 'd':
					delete_entry(conn, [row[0], row[2]])
					result.append(row[0])
					break
				case 'e':
					if edit_entry(conn, 'staging', [row[0], row[2]]) == True:
						add_entry(conn, [row[0], row[2]])
						result.append(row[0])
					break
				case 's':
					logger.info("Skipping query...")
					break
				case 'q':
					logger.info("Quit validation process...")
					conn.commit()
					return result
				case _:
					logger.warning("Undefined input, try again...")
	
	logger.info("All data validated")
	return result
	
