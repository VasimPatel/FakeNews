# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-10 17:49:29
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 21:16:08

import os
import psycopg2
import psycopg2.extras
from functools import wraps

import Utils.settings as settings

# -----------------------
# | CONNECTION WRAPPERS |
# -----------------------

# Creates a new connection and cursor which it passes to the function
def new_connection(host = os.environ.get("DBHOST"), dbname = os.environ.get("DBNAME"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"), primary = False, pass_to_function = True):
	def uses_db_dec(func):
		@wraps(func)
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
				if primary:
					print("Connection stored as the primary connection for easy access.")
					set_primary_cc(connection = connection, cursor = cursor)
					if pass_to_function:
						resp = func(settings.primary_connection, settings.primary_cursor, *args, **kwargs)
					else:
						resp = func(*args, **kwargs)
				else:
					if pass_to_function:
						resp = func(connection, cursor, *args, **kwargs)
					else:
						print("NOTE::You did not make the connection you opened primary and did not pass it to the function that opned it.")
						print("NOTE::Therefore you have no way to access your connection.")
						print("NOTE::Check the pass_to_function parameter to make sure it is set to True if you do not intend to make the connection primary.")
						resp = func(*args, **kwargs)

				connection.commit()
				print("\nCommited changes for this connection.")

				if primary:
					close_cursor(cursor = cursor)
					close_connection(connection = connection)
				else:
					cursor.close()
					connection.close()
					print("Closed connection.\n")

				return resp
			except Exception as e:
				print("\nSomething bad happened while the function was evaluating.")
				print("Changes made WILL NOT BE committed.")
				print("Error will be raised after the connection is closed")

				if primary:
					close_cursor(cursor = cursor)
					close_connection(connection = connection)
				else:
					cursor.close()
					connection.close()
					print("Closed connection.\n")

				raise e

		return wrapper
	return uses_db_dec

# Commits the passed in connection
def commits_connection(func):
	@wraps(func)
	def wrapper(*args, connection = None, cursor = None, **kwargs):
		try:
			if connection == None:
				connection = settings.primary_connection
			if cursor == None:
				cursor = settings.primary_connection

			resp = func(connection, cursor, *args, **kwargs)

			connection.commit()

			return resp
		except Exception as e:
			print("An execption occured while trying to evaluate a function which was supposed to commit.")
			print("Changes made WILL NOT BE committed.")
			print(e)

			raise e

	return wrapper

def defaults_connection_to_primary(func):
	@wraps(func)
	def wrapper(*args, connection = None, **kwargs):
		if connection is None:
			connection = settings.primary_connection

		return func(*args, connection = connection, **kwargs)
	return wrapper

def defaults_cursor_to_primary(func):
	@wraps(func)
	def wrapper(*args, cursor = None, **kwargs):
		if cursor is None:
			cursor = settings.primary_cursor

		return func(*args, cursor = cursor, **kwargs)
	return wrapper

def defaults_connection_and_cursor_to_primary(func):
	@wraps(func)
	def wrapper(*args, connection = None, cursor = None, **kwargs):
		if connection is None:
			connection = settings.primary_connection
		if cursor is None:
			cursor = settings.primary_cursor

		return func(*args, connection = connection, cursor = cursor, **kwargs)
	return wrapper

# Query an return results from database
def execute_as_database_query(func):
	@wraps(func)
	def wrapper(*args, cursor = None, **kwargs):
		if cursor is None:
			cursor = settings.primary_cursor

		resp = func(*args, **kwargs)

		query_string = resp[0]
		query_variables = resp[1]
		if query_variables is None:
			cursor.execute(query_string)
		else:
			cursor.execute(cursor.mogrify(query_string, query_variables))

		result = cursor.fetchall()

		# Standardizes the return so that it always returns a list
		return result if result else [None]
	return wrapper

# Executes the returned string and tuple of the function through the glc
def execute_as_database_command(func):
	@wraps(func)
	def wrapper(*args, connection = None, cursor = None, **kwargs):
		if connection is None:
			connection = settings.primary_connection
		if cursor is None:
			cursor = settings.primary_cursor

		resp = func(*args, **kwargs)

		command_string = resp[0]
		command_variables = resp[1]
		if command_variables is None:
			cursor.execute(command_string)
		else:
			cursor.execute(cursor.mogrify(command_string, command_variables))

		connection.commit()
	return wrapper

def execute_as_database_values_command(func):
	@wraps(func)
	def wrapper(*args, connection = None, cursor = None, **kwargs):
		if connection is None:
			connection = settings.primary_connection
		if cursor is None:
			cursor = settings.primary_cursor

		resp = func(*args, **kwargs)

		command_string = resp[0]
		command_variables = resp[1]
		cursor.execute(command_string, command_variables)

		connection.commit()
	return wrapper

# -----------------------
# | CONNECTION WRAPPERS |
# -----------------------

# Get the primary connection object from settings
def get_primary_connection():
	return settings.primary_connection

# Get the primary cursor object from settings
def get_primary_cursor():
	return settings.primary_cursor

# Open a new cursor object from the given connection
def open_new_cursor(connection):
	# Gets a cursor with dictionary capabilities (returns a dictionary accessable by name)
	cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
	print("Opened a new cursor.")

	return cursor

# Open a new connection (defaults to the .env file variables)
def open_new_connection(host = os.environ.get("DBHOST"), dbname = os.environ.get("DBNAME"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS")):
	try:
		connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (dbname, user, host, password))
		print("\nConnection opened to [dbname:%s] on [host:%s]" % (dbname, host))
		print("Logged in as [user:%s]\n" % user)
	except Exception as e:
		print("\nFailed to connect to the database.")
		print("Tried to connect to [dbname:%s] on [host:%s] as [user:%s]" % (dbname, host, user))
		print("Make sure you have a .env file that that the DBNAME, DBUSER, DBHOST, and DBPASS keys are all correct.")
		raise e
		return

	return connection

# Close the passed in cursor
@defaults_cursor_to_primary
def close_cursor(cursor):
	cursor.close()
	print("Closed open cursor.")
	cursor = None

# Close the passed in connection
@defaults_connection_to_primary
def close_connection(connection):
	connection.close()
	print("Closed connection.")
	connection = None

# Set the primary connection and cursor to the passed in connection and cursor
def set_primary_cc(connection = None, cursor = None):
	if connection == None:
		settings.primary_connection = open_new_connection()
		settings.primary_cursor = open_new_cursor(settings.primary_connection)
	elif cursor == None:
		cursor = open_new_cursor(connection)
		settings.primary_cursor = cursor
	else:
		settings.primary_connection = connection
		settings.primary_cursor = cursor

	print("Primary connection set.\n")

# Execute a database query with the given tuple of variables (the query string should be formatted with % formats for each variable)
@execute_as_database_query
def execute_db_query(query_string, query_variables = None):
	return (query_string, query_variables)

# Execute a database command with the given tuple of variables (the query string should be formatted with % formats for each variable)
@execute_as_database_command
def execute_db_command(command_string, command_variables = None):
	return (command_string, command_variables)

@execute_as_database_values_command
def execute_db_values_command(command_string, command_variables):
	return (command_string, command_variables)
