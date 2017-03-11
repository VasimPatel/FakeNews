# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 14:07:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-10 16:13:20

import Utils.settings as settings
settings.init()

import os
import Utils.db_utils as db_utils
import Utils.get_fakenews_db as db

# def self_reference(func):
# 	import functools
# 	@functools.wraps(func)
# 	def wrapper(*args, **kwargs):
# 		return func(func, *args, **kwargs)
# 	return wrapper

@db_utils.new_connection(host = os.environ.get("DBHOST"), dbname = os.environ.get("DBNAME"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"), global_conn = True)
def main(glc):
	print("You have properly connected to the database!")
	print("Whoohooo!")

	print("\nYou should now see a list of tables in the database...")
	glc.cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
	print(glc.cur.fetchall())
	db.get_tags_named(["Elections", "Elections 2016"])

	print("\nEverything if everything seemed to print correctly you should be connected.")

if __name__ == "__main__":
	main()
