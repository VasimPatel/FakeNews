# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-06 18:54:50
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-10 16:35:17

import os
from dotenv import load_dotenv, find_dotenv



def init():
	# Load the environment file
	# This load makes sure passwords are not stored on github
	# Basically here for security reasons
	load_dotenv(find_dotenv())
	# This is basically the glc
	# These two varaibles can be access by importing settings and using 'settings.conn' or 'settings.cur'
	global conn
	conn = None
	global cur
	cur = None

# Set the global connection variables to the given connection and cursor
def set_global_connection(connection, cursor):
	conn = connection
	cur = cursor

# Close the global connection and reset the variables to None
def close_global_connection():
	cur.close()
	conn.close()
	print("Global connection was closed.")
	conn = None
	cur = None
