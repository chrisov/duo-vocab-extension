import sqlite3 as sql
from .JSONVocab import JSONVocab
from app.server_utils import get_path
from .daemon_utils import get_active_session
import os

def _init_sql():
	db = get_path("DB")
	conn = sql.connect(db)
	cursor = conn.cursor()
	cursor.execute('''
			CREATE TABLE IF NOT EXISTS staging_approved (
			Word TEXT PRIMARY KEY,
			Language TEXT NOT NULL,
			Article TEXT,
			English TEXT NOT NULL,
			Plural TEXT,
			Grammar TEXT NOT NULL,
			Category TEXT NOT NULL,
			Difficulty TEXT NOT NULL,
			Count INTEGER NOT NULL DEFAULT 0,
			SuccessRate REAL NOT NULL DEFAULT 0.0
			);
			''')
	conn.commit()
	return cursor



def staging(obj: JSONVocab):
	approved = obj.get_approved()
	disapproved = obj.get_disapproved()

	print(approved)
	print(disapproved)



if __name__ == "__main__":

	cursor = _init_sql()
	obj = JSONVocab("VOCAB_PATH", get_active_session())
	staging(obj)