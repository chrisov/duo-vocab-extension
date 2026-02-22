from daemon.JSONVocab import JSONVocab
from daemon.daemon_utils import get_active_session
from .sql_utils import populate_staging, print_table
import sqlite3 as sql
import logging

logger = logging.getLogger(__name__)

def staging(conn:sql.Connection):
	"""
	
	"""

	## TODO check if table is already populated

	obj = JSONVocab("VOCAB_PATH", get_active_session())
	approved = obj.get_approved()
	populate_staging(conn, 'staging', obj.get_language(), approved)


from examiner.sql_utils import init_sql
if __name__ == "__main__":

	conn = init_sql()
	staging(conn)
	print_table(conn, 'staging')
	conn.close()
