# @Author: DivineEnder
# @Date:   2017-03-21 23:45:32
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-13 09:43:11

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
	sys.stdout.write("\r[%s] %d/%d (%02d%%)  ETA (full runtime): %s  ETA (indv. runtime): %s" % (("#" * display_percent) + (" " * (bar_length - display_percent)),
		progress,
		max_progress,
		percent * 100,
		str(time_to_finish_cest),
		str(time_to_finish_lest)))

def loop_display_progress(l, func, *func_args):
	# Track total runtime
	total_runtime = 0
	# Set the last progress display time to the current time
	lpd_time = datetime.datetime.now()
	# Loop through passed in list
	for i in range(0, len(l)):
		# execute the given function on the list element and all other args passed to function
		runtime = time_it(func, l[i], *func_args)
		# Total runtime of whole process
		total_runtime = total_runtime + runtime
		# Display only updates after at least 1 second has passed
		if (datetime.datetime.now() - lpd_time) > datetime.timedelta(seconds = 1):
			# Display progress bar
			progress_bar(50, i+1, len(l), cur_runtime = total_runtime, last_runtime = runtime)
			# Update the last progress display time
			lpd_time = datetime.datetime.now()

	print()
