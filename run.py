# @Author: DivineEnder
# @Date:   2017-04-10 20:44:40
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 21:16:46

from Utils import settings
settings.init()
import sys

from importlib import import_module

def main():
	script = sys.argv[1:2][0].replace("/", ".").replace("\\", ".")
	mod = import_module(script)
	if len(sys.argv) > 4:
		mod.main(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10])
		#name_scheme, load_lda, load_bayes, load_svm, run_tests, num_articles, num_train, lda_only, bayes_only
	else:
		mod.main()

if __name__ == "__main__":
	main()
