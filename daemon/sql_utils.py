from app.server_utils import get_path
import sqlite3 as sql
import tabulate as tbl
import os
import logging


logger = logging.getLogger(__name__)


def print_tables(cursor: sql.Cursor):
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()

	print("\n========= TABLES =========")
	for t in tables:
		print(f"- '{t[0]}'")
	print("=" * 26 + "\n")



def init_sql() -> sql.Connection:
	db = get_path("DB")

	logger.info("Checking DB")
	existed = True if os.path.exists(db) else False
	conn = sql.connect(db)
	cursor = conn.cursor()

	if existed:
		logger.info(f"Connecting to '{db}'...")
	else:
		logger.info(f"Creating '{db}': Initializing tables...")
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
					Word TEXT PRIMARY KEY,
					Article TEXT,
					Language TEXT NOT NULL,
				 	English TEXT NOT NULL,
					Plural TEXT,
					Grammar TEXT NOT NULL,
					Category TEXT NOT NULL,
					Difficulty TEXT NOT NULL,
					Count INTEGER NOT NULL DEFAULT 0,
					SuccessRate REAL NOT NULL DEFAULT 0.0);
				''')

		## Init vocabulary table
		cursor.execute('''
				CREATE TABLE IF NOT EXISTS vocabulary (
					Word TEXT PRIMARY KEY,
					Article TEXT,
					Language TEXT NOT NULL,
					Plural TEXT,
					Grammar TEXT NOT NULL,
					Category TEXT NOT NULL,
					Difficulty TEXT NOT NULL,
					Count INTEGER NOT NULL DEFAULT 0,
					SuccessRate REAL NOT NULL DEFAULT 0.0);
				''')

		cursor.execute('''
				CREATE TABLE IF NOT EXISTS translation (
					Word     TEXT    NOT NULL,
					English  TEXT    NOT NULL,
					PRIMARY KEY (Word, English),
					FOREIGN KEY (Word) REFERENCES vocabulary(Word) ON DELETE CASCADE);
				''')
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()
	conn.commit()
	logger.info(f"Tables: {[t[0] for t in tables]}")
	logger.info(f"'{db}': Connection established")
	return conn



def populate_table(conn: sql.Connection, table_name: str, lang: str, vocab: list):
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
		except sql.Error as e:
			logger.error(f"Error populating table '{table_name}': {str(e)}")
	conn.commit()



def print_table(conn: sql.Connection, table_name: str):
	cursor = conn.cursor()
	cursor.execute(f"SELECT * FROM {table_name}")
	rows = cursor.fetchall()
	columns = [description[0] for description in cursor.description]
	print("\n" + tbl.tabulate(rows, headers=columns, tablefmt='fancy_grid'))
	print(f"Table name: '{table_name}'")
