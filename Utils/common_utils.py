# @Author: DivineEnder
# @Date:   2017-03-21 23:45:32
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-22 00:05:48

import sys
import datetime
import timeit

def time_it(func, *args, **kwargs):
	def eval_func():
		return func(*args, **kwargs)
	return timeit.timeit(eval_func, number = 1)

def progress_bar(bar_length, progress, max_progress, cur_runtime = None, last_runtime = None, specificity = 2):
	percent = round(float(progress)/float(max_progress), specificity)
	display_percent = int(percent * bar_length)

	if not last_runtime is None:
		seconds_left = int((max_progress - progress) * last_runtime)
		time_to_finish_lest = datetime.timedelta(seconds = seconds_left)
	else:
		time_to_finish_lest = "Not avaliable"

	if not cur_runtime is None:
		rate = (float(progress)/float(max_progress))/float(cur_runtime)
		seconds_left = int((1 - percent)/rate)
		time_to_finish_cest = datetime.timedelta(seconds = seconds_left)
	else:
		time_to_finish_cest = "Not avaliable"

	sys.stdout.flush()
	sys.stdout.write("\r%s" % (" " * (bar_length*3)))# + len(str(time_to_finish)))))
	sys.stdout.flush()
	sys.stdout.write("\r[%s]  %02d%%  ETA (full runtime): %s  ETA (indv. runtime): %s" % (("#" * display_percent) + (" " * (bar_length - display_percent)),
		percent * 100,
		str(time_to_finish_cest),
		str(time_to_finish_lest)))
