# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-06 18:54:50
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivinePC
# @Last modified time: 2017-03-06 18:59:21

from dotenv import load_dotenv, find_dotenv

def init():
	# Load the environment file
	# This load makes sure passwords are not stored on github
	# Basically here for security reasons
	load_dotenv(find_dotenv())
