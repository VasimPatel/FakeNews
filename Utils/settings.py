# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-06 18:54:50
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-29 15:05:38 

import os
from dotenv import load_dotenv, find_dotenv

def init():
	# Load the environment file
	# This load makes sure passwords are not stored on github
	# Basically here for security reasons
	load_dotenv(find_dotenv())
	# This is basically the glc
	# These two varaibles can be access by importing settings and using 'settings.conn' or 'settings.cur'
	global primary_connection
	primary_connection = None
	global primary_cursor
	primary_cursor = None
