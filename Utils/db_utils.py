# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-04 23:42:57
# @Last modified by:   DivinePC
# @Last modified time: 2017-03-06 20:42:58

import psycopg2
import functools

# -----------------------
# | CONNECTION WRAPPERS |
# -----------------------
def new_connection(host, dbname, user, password):
	def uses_db_dec(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			try:
				connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (dbname, user, host, password))
				print("\nConnection opened to [dbname:%s] on [host:%s]" % (dbname, host))
				print("Logged in as [user:%s]\n" % user)
			except Exception as e:
				print("\nFailed to connect to the database.")
				print("Tried to connect to [dbname:%s] on [host:%s] as [user:%s]" % (dbname, host, user))
				print("Make sure you have a .env file that that the DBNAME, DBUSER, DBHOST, and DBPASS keys are all correct.")
				return

			cursor = connection.cursor()

			try:
				resp = func(connection, cursor, *args, **kwargs)

				connection.commit()
				print("Commited changes for this connection.")
			except Exception as e:
				print("Something bad happened while the function was evaluating.")
				print("Changes made WILL NOT BE committed.")
				print(e)

			cursor.close()
			connection.close()
			print("Closed connection.\n")

			return resp

		return wrapper
	return uses_db_dec

def commits_connection(func):
	@functools.wraps(func)
	def wrapper(connection, cursor, *args, **kwargs):
		resp = func(connection, cursor, *args, **kwargs)

		connection.commit()

		return resp
	return wrapper
# -----------------------
# | CONNECTION WRAPPERS |
# -----------------------

# --------------------
# | GENERIC DB UTILS |
# --------------------
@commits_connection
def add_table_to_db(conn, cur, table_name, *cols, VERBOSE = True):
	cols_string = ""
	for col in cols:
		cols_string = cols_string + col + ", "
	cols_string = cols_string[0:-2]
	print(cols_string)
	SQL_cmd = "CREATE TABLE %s (%s)" % (table_name, cols_string)
	cur.execute(SQL_cmd)
	if VERBOSE:
		print("Added %d table with columns: ")
		for col in cols:
			print("  %s" % col)

@commits_connection
def add_column_to_table(conn, cur, table, col_name, col_type, VERBOSE = False):
	SQL_cmd = "ALTER TABLE %s ADD COLUMN %s %s" % (table, col_name, col_type)
	cur.execute(SQL_cmd)
	if VERBOSE:
		print("Added column %s to %s table [type:%s]." % (table, col_name, col_type))

@commits_connection
def drop_column_from_table(conn, cur, table, col_name, VERBOSE = False):
	SQL_cmd = "ALTER TABLE %s DROP COLUMN %s" % (table, col_name)
	cur.execute(SQL_cmd)
	if VERBOSE:
		print("Dropped column %s from %s table." % (col_name, table))

@commits_connection
def set_column_default(conn, cur, table, col_name, default_val, VERBOSE = False):
	SQL_cmd = "ALTER TABLE %s ALTER COLUMN %s SET DEFAULT %f" % (table, col_name, float(default_val))
	cur.execute(SQL_cmd)
	if VERBOSE:
		print("Set default for %s in %s table to %s." % (col_name, table, default_val))

@commits_connection
def drop_column_default(conn, cur, table, col_name, VERBOSE = False):
	SQL_cmd = "ALTER TABLE %s ALTER COLUMN %s DROP DEFAULT" % (table, col_name)
	cur.execute(SQL_cmd)
	if VERBOSE:
		print("Dropped default for %s in %s table.")

def drop_constraint_from_table(conn, cur, table, cons_name, VERBOSE = False):
	SQL_cmd = "ALTER TABLE %s DROP CONSTRAINT %s" % (table, cons_name)
	cur.execute(SQL_cmd)
	if VERBOSE:
		print("Dropped %s constraint from %s table" % (cons_name, table))
# --------------------
# | GENERIC DB UTILS |
# --------------------
