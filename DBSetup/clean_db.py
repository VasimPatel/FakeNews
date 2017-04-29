# @Author: DivineEnder
# @Date:   2017-04-21 13:26:19
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-21 13:52:07 


import Utils.connection_utils as glc

def clean_zero_content_articles():
	glc.execute_db_command("""DELETE FROM articles WHERE content SIMILAR TO '( |\t|\r|\n)*';""")

glc.new_connection(primary = True, pass_to_function = False)
def main():
	clean_zero_content_articles()
