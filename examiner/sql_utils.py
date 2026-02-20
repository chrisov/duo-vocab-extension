import sqlite3 as sql


def populate_translation(conn: sql.Connection, translations: list):

	# Enable Foreign Key support (SQLite turns this OFF by default!)
	conn.execute("PRAGMA foreign_keys = ON;") 
	cursor = conn.cursor()

	try:
		cursor.executemany('''
			INSERT INTO translation (Word, English) 
			VALUES (?, ?)
		''', translations)
		conn.commit()
		print(f"Successfully added {cursor.rowcount} translations.")
	except sql.IntegrityError as e:
		print(f"Error: {e}")
		print("Hint: Make sure the 'Word' exists in the 'staging' table first!")

	conn.close()
