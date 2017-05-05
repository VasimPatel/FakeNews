from sklearn.externals import joblib

def important(words, val):
	if val > 0:
		return sorted(words,key=lambda l: (l[1]))[:val]
		#return sorted(words,key=lambda l: (l[1]))[:10000]
	else:
		return sorted(words,key=lambda l: (l[1]))[len(words)+val:][::-1]
		#return sorted(words,key=lambda l: (l[1]))[:10000]


def main():
	name = 'loadAndsave/important_words/15_linear_300_150_150'
	out_file = open(name + '.csv', 'w')
	dictionary = joblib.load('loadAndsave/bayes_dict/15_linear_300_150_150.pkl')

	real_dict = dictionary['real']
	fake_dict = dictionary['fake']

	results = []

	for each_word, fake_val in fake_dict.items():
		if real_dict.get(each_word) is not None:
			real_val = real_dict[each_word]
			print(real_val)
		else:
			real_val = 15

		rel_val = fake_val - real_val

		results.append([each_word, rel_val])


	
	# top 25 for fake
	important_fake = important(results, 25)

	# top 25 real
	important_real = important(results, -25)

	print("\n\n{0:<7} {1:<16} {2:<16} {3:<13} {4:<16}".format("Rank", "Fake","Fake Weight", "Real", "Real Weight"))
	print("--------------------------------------------------------")
	out_file.write("{}, {}, {}, {}, {}".format("Rank", "Fake","Fake Weight", "Real", "Real Weight"))
	i = 1
	for fake_word, real_word in zip(important_fake, important_real):
		print("{0:<5} {1:<15} {2:<15} {3:<15} {4:<15}".format(str(i), fake_word[0], round(fake_word[1],3), real_word[0], round(real_word[1],3)))
		out_file.write("\n{0}, {1}, {2}, {3}, {4}".format(str(i), fake_word[0], round(fake_word[1],3), real_word[0], round(real_word[1],3)))
		i+=1

	r = []
	# for e, v in fake_dict.items():
	# 	r.append([e,v])
	# r = sorted(r,key=lambda l: (l[1]))[:100]
	# for each in r:
	# 	print(each[0])








