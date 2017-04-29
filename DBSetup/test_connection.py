# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 14:07:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 20:35:24

import os
from Utils import db_utils
from Utils import connection_utils as glc
from Utils import get_db_utils as db

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	print("You have properly connected to the database!")
	print("Whoohooo!")

	print("\nYou should now see a list of tables in the database...")
	db_utils.list_all_db_tables()

	print("\nIf everything seemed to print correctly you should be connected.")

if __name__ == "__main__":
	main()
