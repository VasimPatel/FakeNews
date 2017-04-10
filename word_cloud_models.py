import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
MODELS_DIR = "topic_modeling/models"

final_topics = open(os.path.join(MODELS_DIR, "final_topics.txt"), 'r')
curr_topic = 0
for line in final_topics:
    #line = line.strip()[line.rindex(":") + 2:]
    scores = [float(x.split("*")[0]) for x in line.split(" + ")]
    words = [x.split("*")[1] for x in line.split(" + ")]
    freqs = {}
    for word, score in zip(words, scores):
        freqs[word] = score
    wordcloud = WordCloud(width=120, height=120).generate_from_frequencies(freqs)
    curr_topic += 1
    # lower max_font_size
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
final_topics.close()