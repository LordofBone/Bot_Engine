### Setup

##### Installation

Ensure you have git installed and get Bot Engine and the Chatbot with:

`git clone --recursive https://github.com/LordofBone/Bot_Engine`

##### eSpeak setup

The Bot Engine is designed to use eSpeak as its native TTS; but there is no reason why this cannot be changed to use 
something else.



##### Setting up the Chatbot and Sentiment models

First ensure you have a PostgreSQL server setup as per the instructions of the 
Chatbot - https://github.com/LordofBone/Chatbot_8#docker-postgresql-installation

Drop a training file into the Chatbot data path (the same instructions for the training file for the chatbot apply
here - https://github.com/LordofBone/Chatbot_8#training-the-bot):

`Chatbot_8/data/training/`

Run:

`python \utils\bot_db_control.py -o TRAIN`

This should also install the submodule 'Chatbot_8' using the command:

`pip install -e Chatbot_8/`

If you would prefer to run this yourself, you can. This is a bit of a hacky way to get around the weird directory 
structure stuff you have to deal with in Python; I find that if I just import stuff from the Chatbot_8 directory 
it has trouble finding the /data/training folders and stuff as Python likes to be relative to the file it's initially 
being run from.

If anyone knows a better way around this than using the above pip install method, let me know.

After that it will then train the bot from the training data supplied, and also train a markovify model for the bot 
and put it under Chatbot_8/models/markovify/bot_1.

After that you will need to run the sentiment training:

`python utils/sentiment_training_suite.py`

Which will then download a set of various NLTK + Tensorflow datasets and models and the train on them.

The bot should now be installed, setup and ready to go.

##### Running the Bot Engine

Should be as simple as:

`python launch_ai.py`

##### Configuration

Under the config folder there are a number of files:

###### emotion_config.py

You can configure what sentiment analysis engine is being used here as well as the amount of previous sentiments 
to keep in memory to average out.

The thresholds for what are considered a positive and a negative mood are also set here, as well as the initial mood 
on startup.

###### gui_config.py

Config for window name, colour and whether the GUI is activated.

###### nltk_config.py

Contains locations for all the NLTK models and datasets.

###### tensorflow_config.py

Contains locations for all the Tensorflow models and datasets as well as training configuration such as epochs etc.

###### voice_config.py

Here audio can be switched on or off and the varying levels of the Chatbots pitch and cadence can be adjusted.