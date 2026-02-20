from .JSONVocab import JSONVocab
from .daemon_utils import get_active_session
from .sql_utils import populate_table, print_table
import sqlite3 as sql
import logging

logger = logging.getLogger(__name__)

def staging(conn:sql.Connection, obj: JSONVocab):
	"""
	
	"""
	approved = obj.get_approved()
	populate_table(conn, 'staging', obj.get_language(), approved)
	logger.info("'staging' table was populated")



from .sql_utils import init_sql
if __name__ == "__main__":

	conn = init_sql()
	obj = JSONVocab("VOCAB_PATH", get_active_session())
	staging(conn, obj)
	print_table(conn, 'staging')
	conn.close()
