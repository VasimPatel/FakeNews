# @Author: DivineEnder
# @Date:   2017-04-10 21:11:13
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 21:26:45

from textstat.textstat import textstat

def get(article):
	return textstat.text_standard(article['content'])
