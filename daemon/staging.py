import sqlite3 as sql
from .JSONVocab import JSONVocab
from .daemon_utils import get_active_session, clear_list_from_json
from .sql_utils import init_sql, populate_table, print_table

def staging(conn:sql.Connection, obj: JSONVocab):
	approved = obj.get_approved()
	populate_table(conn, 'staging', obj.get_language(), approved)

if __name__ == "__main__":

	conn = init_sql()
	obj = JSONVocab("VOCAB_PATH", get_active_session())
	staging(conn, obj)
	print_table(conn, 'staging')
	conn.close()
