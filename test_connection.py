# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 14:07:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-28 21:31:20

import Utils.settings as settings
settings.init()

import os
import Utils.db_utils as db_utils
import Utils.get_fakenews_db as db

@db_utils.new_connection(primary = True, pass_to_function = False)
def main():
	print("You have properly connected to the database!")
	print("Whoohooo!")

	print("\nYou should now see a list of tables in the database...")
	db_utils.list_all_db_tables()
	db.get_tags_named(["Elections", "Elections 2016"])

	print("\nEverything if everything seemed to print correctly you should be connected.")

if __name__ == "__main__":
	main()
