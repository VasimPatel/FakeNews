# @Author: DivineEnder
# @Date:   2017-03-20 15:05:04
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-20 19:37:11

import Utils.settings as settings
settings.init()

# Import required modules
import os
import Utils.connection_utils as glc
import Utils.db_utils as db_utils

@glc.new_connection(primary = True)
def main(conn, cursor):
	glc.execute_db_command("""DROP SCHEMA public CASCADE""")
	glc.execute_db_command("""CREATE SCHEMA public""")
	glc.execute_db_command("""GRANT ALL ON SCHEMA public TO postgres""")
	glc.execute_db_command("""GRANT ALL ON SCHEMA public TO public""")
	glc.execute_db_command("""COMMENT ON SCHEMA public IS 'standard public schema'""")

if __name__ == "__main__":
	main()
	# glc.open_connection(store_connection = True)
	# glc.open_connection(store_connection = True)
	# try:
	# 	main()
	# except Exception as e:
	# 	glc.close_connection()
	# 	raise(e)
