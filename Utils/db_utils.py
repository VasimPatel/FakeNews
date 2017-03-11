# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-04 23:42:57
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-10 17:46:41

import psycopg2
import Utils.settings as settings
import functools

# -----------------------
# | CONNECTION WRAPPERS |
# -----------------------
# Checks to see whether the global connection is set before the function is run
def checks_glc(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if settings.conn == None or settings.cur == None:
			print("ERROR: Could not use global connection and/or cursor. Was not properly initalized.")
			raise EnvironmentError

		return func(*args, **kwargs)
	return wrapper

# Creates a new connection that it then passes to the global connection object (glc) or the connection and cursor objects (if not global)
def new_connection(host, dbname, user, password, global_conn = False):
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

			# Gets a cursor with dictionary capabilities
			cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

			try:
				# Set the connection to global so that it can be accessed from the settings file
				if global_conn:
					print("This connection is now a global connection.")
					settings.set_global_connection(connection, cursor)
					resp = func(settings, *args, **kwargs)
				else:
					resp = func(connection, cursor, *args, **kwargs)

				connection.commit()
				print("Commited changes for this connection.")

				if global_conn:
					settings.close_global_connection
				else:
					cursor.close()
					connection.close()
					print("Closed connection.\n")

				return resp
			except Exception as e:
				print("Something bad happened while the function was evaluating.")
				print("Changes made WILL NOT BE committed.")
				print("\nError message was:")
				print(str(e) + "\n")

				if global_conn:
					settings.close_global_connection
				else:
					cursor.close()
					connection.close()
					print("Closed connection.\n")

				raise e

		return wrapper
	return uses_db_dec

# Commits the passed in connection
def commits_connection(func):
	@functools.wraps(func)
	def wrapper(connection, cursor, *args, **kwargs):
		try:
			resp = func(connection, cursor, *args, **kwargs)

			connection.commit()

			return resp
		except Exception as e:
			print("An execption occured while trying to evaluate a function which was supposed to commit.")
			print("Changes made WILL NOT BE committed.")
			print(e)

			raise e

	return wrapper

# Passes the glc to the given function
@checks_glc
def uses_glc(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		return func(settings, *args, **kwargs)
	return wrapper

# Passes the glc to the given function and commits it
@checks_glc
def commits_glc(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		try:
			resp = func(settings, *args, **kwargs)

			settings.conn.commit()

			return resp
		except Exception as e:
			print("An execption occured while trying to evaluate a function which was supposed to commit the glc (glocal connection).")
			print("Changes made WILL NOT BE committed.")

			raise e

	return wrapper

# Executes the returned string and tuple of the function through the glc
@checks_glc
@commits_glc
def glc_database_command(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		resp = func(settings, *args, **kwargs)

		command_string = resp[0]
		command_variables = resp[1]
		if query_variables is None:
			settings.cur.execute(command_string)
		else:
			settings.cur.execute(settings.cur.mogrify(command_string, command_variables))
	return wrapper

# Query an return results from database
@checks_glc
def glc_database_query(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		resp = func(settings, *args, **kwargs)

		query_string = resp[0]
		query_variables = resp[1]
		if query_variables is None:
			settings.cur.execute(query_string)
		else:
			settings.cur.execute(settings.cur.mogrify(query_string, query_variables))

		result = settings.cur.fetchall()

		return result if result else [None]
	return wrapper

# -----------------------
# | CONNECTION WRAPPERS |
# -----------------------

@commits_glc
def close_all_db_connections(dbname = None):
	target_db = dbname if dbname else os.environ.get("DBNAME")
	cur.execute(cur.mogrify("""SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();""", (target_db,)))

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
