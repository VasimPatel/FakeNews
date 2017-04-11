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
	mod.main()

if __name__ == "__main__":
	main()
