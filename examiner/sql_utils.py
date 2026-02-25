import sqlite3 as sql
from app.server_utils import get_path
import tabulate as tbl
import os
import logging


logger = logging.getLogger(__name__)


def init_sql() -> sql.Connection:
	db = get_path("DB")

	print()
	logger.info("Checking DB")
	existed = True if os.path.exists(db) else False
	conn = sql.connect(db)
	cursor = conn.cursor()

	if existed:
		logger.info(f"Connecting to '{db}'...")
	else:
		logger.info(f"Creating '{db}': Initializing tables...")
		try:
			## Init description table
			cursor.execute('''
					CREATE TABLE table_descriptions (
						table_name TEXT PRIMARY KEY,
						description TEXT,
						last_updated DATETIME DEFAULT CURRENT_TIMESTAMP);
					''')
			
			## Insert values in description table
			cursor.execute('''
					INSERT INTO table_descriptions (table_name, description) 
					VALUES
						('staging',
						'Queue for submitted word definitions awaiting approval.'),
						('vocabulary',
						'Main dictionary'),
						('translation',
						'Vocabulary translations in English');
					''')

			## Init staging table
			cursor.execute('''
				CREATE TABLE IF NOT EXISTS staging (
						Word TEXT NOT NULL,
						Article TEXT,
						Language TEXT NOT NULL,
						English TEXT NOT NULL,
						Plural TEXT,
						Grammar TEXT NOT NULL,
						Category TEXT NOT NULL,
						Difficulty TEXT NOT NULL,
						Count INTEGER NOT NULL DEFAULT 0,
						SuccessRate REAL NOT NULL DEFAULT 0.0,
						PRIMARY KEY (Word, Language));
					''')

			## Init vocabulary table
			cursor.execute('''
					CREATE TABLE IF NOT EXISTS vocabulary (
						Word TEXT,
						Article TEXT,
						Language TEXT NOT NULL,
						Plural TEXT,
						Grammar TEXT NOT NULL,
						Category TEXT NOT NULL,
						Difficulty TEXT NOT NULL,
						Count INTEGER NOT NULL DEFAULT 0,
						SuccessRate REAL NOT NULL DEFAULT 0.0,
						PRIMARY KEY (Word, Language));
					''')

			## Init translation table
			cursor.execute('''
					CREATE TABLE IF NOT EXISTS translation (
						Word     TEXT    NOT NULL,
						Language TEXT NOT NULL,
						English  TEXT    NOT NULL,
						PRIMARY KEY (Word, Language, English),
						FOREIGN KEY (Word, Language)
							REFERENCES vocabulary (Word, Language)
							ON DELETE CASCADE);
					''')

			cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
			tables = cursor.fetchall()
			conn.commit()

			logger.info(f"Tables: {[t[0] for t in tables]}")
			logger.info(f"'{db}': Connection established")

		except sql.Error as e:
			conn.rollback()
			logger.error(f"Init tables: Transaction failed, rolled back: {str(e)}")
			raise e
	logger.info(f"Connection established to DB: '{db}'")
	return conn



def init_staging(conn: sql.Connection, table_name: str, lang: str, vocab: list):

	if not vocab:
		logger.info("No new vocabulary detected")
		return

	cursor = conn.cursor()
	for row in vocab:
		try:
			cursor.execute(
				f"""
				INSERT OR IGNORE INTO {table_name} (
					Word, Article, Language, English, Plural,
					Grammar, Category, Difficulty, Count, SuccessRate
				) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
				""",
				(
					row.get("Word"),
					row.get("Article"),
					lang,
					row.get('English'),
					row.get("Plural"),
					row.get("Grammar"),
					row.get("Category"),
					row.get("Difficulty"),
					row.get("Count", 0),
					row.get("SuccessRate", 0.0),
				),
			)
			conn.commit()
		except sql.Error as e:
			conn.rollback()
			logger.error(f"Error populating table '{table_name}': {str(e)}")
	logger.info("New vocabulary detected")



def validate_all_disapproved(conn: sql.Connection, commit: bool = False):
	pass



def	populate_vocabulary(conn: sql.Connection, commit: bool = False):
	cursor = conn.cursor()

	try:
		cursor.execute('''INSERT OR IGNORE INTO vocabulary (
						Word,
						Article,
						Language,
						Plural,
						Grammar,
						Category,
						Difficulty,
						Count,
						SuccessRate),
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
		if commit == True:
			conn.commit()
		logger.info("All entries approved ")
	except sql.Error as e:
		conn.rollback()
		logger.error(f"'vocabulary': Transaction 'validate all' failed, rolled back: '{str(e)}'")



def print_tables(cursor: sql.Cursor):
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()

	print("\n========= TABLES =========")
	for t in tables:
		print(f"- '{t[0]}'")
	print("=" * 26 + "\n")



def print_table(conn: sql.Connection, table_name: str):
	
	cursor = conn.cursor()

	cursor.execute(f"SELECT * FROM {table_name}")
	rows = cursor.fetchall()
	columns = [description[0] for description in cursor.description]

	print("\n" + tbl.tabulate(rows, headers=columns, tablefmt='fancy_grid'))
	print(f"Table name: '{table_name}'")



def print_row(conn: sql.Connection, table_name:str, keys: list):
	
	cursor = conn.cursor()

	try:
		cursor.execute(f"""SELECT * FROM {table_name}
					WHERE Word = ?
					AND Language = ?""", keys)
		rows = cursor.fetchall()
		columns = [description[0] for description in cursor.description]
	except sql.Error as e:
		conn.rollback()
		logger.error(f"Print {keys} in '{table_name}': Transaction failed, rolled back: {str(e)}")

	print("\n" + tbl.tabulate(rows, headers=columns, tablefmt='fancy_grid'))



def populate_one_vocabulary(conn: sql.Connection, keys: list, commit: bool = False, msg: bool = False):
	cursor = conn.cursor()

	try:
		cursor.execute("""
			INSERT OR IGNORE INTO vocabulary (
				Word,
				Article,
				Language,
				Plural,
				Grammar,
				Category,
				Difficulty,
				Count,
				SuccessRate
			)
			SELECT
				Word,
				Article,
				Language,
				Plural,
				Grammar,
				Category,
				Difficulty,
				Count,
				SuccessRate
			FROM staging
			WHERE Word = ? AND Language = ?
		""", keys)
		if commit == True:
			conn.commit()
		if msg == True:
			logger.info(f"Approved entry: {keys} ✅")
	except sql.Error as e:
		conn.rollback()
		logger.error(f"Populate 'vocabulary': Transaction {keys} failed, rolled back: '{str(e)}'")
		raise e



def populate_one_translation(conn: sql.Connection, keys: list, commit: bool = False):

	# Enable Foreign Key support (SQLite turns this OFF by default!)
	conn.execute("PRAGMA foreign_keys = ON;") 
	cursor = conn.cursor()

	try:
		cursor.execute("""
			INSERT OR IGNORE INTO translation (
				Word,
				Language,
				English
			)
			SELECT
				Word,
				Language,
				English
			FROM staging
			WHERE Word = ? AND Language = ?
		""", keys)
		if commit == True:
			conn.commit()
	except sql.Error as e:
		conn.rollback()
		logger.error(f" Populate 'translation': Transaction {keys} failed, rolled back: '{str(e)}'")
		raise e



def delete_one(conn: sql.Connection, table_name: str, keys: list, commit: bool = False, msg: bool = False):
	cursor = conn.cursor()

	try:
		cursor.execute(f"""DELETE FROM {table_name}
				WHERE Word = ?
				AND Language = ?""",
			keys)
		if commit == True:
			conn.commit()
		if msg:
			logger.info(f"Deleted entry: {keys} 🗑️")
	except sql.Error as e:
		conn.rollback()
		logger.error(f"'delete': Transaction {keys} failed, rolled back: '{str(e)}'")
		raise e



def update_query(conn: sql.Connection, table_name: str, pair_value: list, keys: list, commit: bool = False):
	cursor = conn.cursor()

	try:
		cursor.execute(f"""UPDATE {table_name}
			SET {pair_value[0]} = ?
			WHERE Word = ? AND Language = ?""", (pair_value[1], *keys))
		logger.info(f"Updated entry: {pair_value} 🔄")
		if commit == True:
			conn.commit()
	except sql.Error as e:
		conn.rollback()
		logger.error(f"'{table_name}': Transaction {keys} failed, rolled back: {str(e)}")



def append_to_column(conn: sql.Connection, table_name: str, pair_value: list, keys:list, commit: bool = False):
	cursor = conn.cursor()

	try:
		cursor.execute(f"""
			UPDATE {table_name}
			SET {pair_value[0]} = CASE
				WHEN {pair_value[0]} = '' OR {pair_value[0]} IS NULL THEN ?
				ELSE {pair_value[0]} || '|' || ?
			END
			WHERE Word = ? AND Language = ?""",
				(pair_value[1], pair_value[1], *keys));
		logger.info(f"'{table_name}': Append to {keys} -> {pair_value}")
		if commit == True:
			conn.commit()
	except sql.Error as e:
		conn.rollback()
		logger.error(f"'{table_name}': Appending {pair_value} to {keys} failed, rolled back: '{str(e)}'")

