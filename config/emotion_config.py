process_emotions = True

engines = ['nltk-vader', 'nltk-twitter', 'tensorflow']
emotion_engine = engines[2]
max_emotion_short_memory = 5

initial_emotion_average = 0
negative_emotion_threshold = -0.150
positive_emotion_threshold = 0.150
