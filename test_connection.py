# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 14:07:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-08 14:07:51

@db_utils.new_connection(host = os.environ.get("DBHOST"), dbname = os.environ.get("DBNAME"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"))
def main(conn, cur):
	print("You have properly connected to the database!")
	print("Whoohooo!")

if __name__ == "__main__":
	main()
