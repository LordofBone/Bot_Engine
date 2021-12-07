### What is the Bot Engine?

This is essentially a framework for someone to use to create their own intelligent Bot, it is designed to be modular 
and editable - so someone can create their own frontend, change the default voices/animations for the GUI etc. Or even 
implement their own interface for a GUI or pipe out the outputs to something like a robot head/face.

It uses Chatbot_8: https://github.com/LordofBone/Chatbot_8 for the responses, which is included as a submodule which 
is also customisable on what it is trained on.

The Bot Engine adds another layer of sentiment analysis (which over time will be evolved to cover actual emotions, 
rather than just positive/negative responses) and as mentioned the ability to output the responses via audio/visual 
means.

At the moment the default voices are the eSpeak voices and a couple of sound snippets from CABAL from the video game 
Command and Conquer: Tiberian Sun: https://cnc-central.fandom.com/wiki/Computer_Assisted_Biologically_Augmented_Lifeform

So feel free to take the code/framework and make your own bots with it.

### Setup

##### Installation

###### Essential setup + Windows/Linux x86-64

Ensure you have Python 3.9 installed (this is what I have been using for it so far).

Install Docker:

Windows - https://docs.docker.com/desktop/windows/install/
Linux - use the script under Chatbot_8/build:

`install_docker_linux.sh`

Then run:

`sudo usermod -aG docker "$USER"`

Then reboot.

Ensure you have git installed and get Bot Engine and the Chatbot with:

`git clone --recursive https://github.com/LordofBone/Bot_Engine`

On Linux+RPi you will also need to ensure an additional library is installed for pyscopg2:

`sudo apt-get install libpq-dev`

Although if you build the Chatbot Docker container from the script under Chatbot_8/Build/install_docker_linux.sh, this
will install it for you.

Then set up a python venv (https://docs.python-guide.org/dev/virtualenvs/) and install the requirements:

`pip install -r requirements.txt`

###### Raspberry Pi OS 64-bit ARM specific setup

When it comes to installing this on a Raspberry Pi at the time of writing you will need to do the above, but also
you will need the 64 bit version of the RPI OS (Bullseye) - https://downloads.raspberrypi.org/raspios_arm64/images/ 
which you can install to an SD card with the imager: https://www.raspberrypi.com/software/

The above requirements should still install everything needed, then stop at tensorflow and tensorflow-gpu.

This is where at the moment, some manual intervention is required:

Go here and download the wheel for 2.7.0 Python 3 64 Bit ARM:
https://github.com/Qengineering/TensorFlow-Raspberry-Pi_64-bit

Then while still in the venv made above:

`PIP_EXTRA_INDEX_URL=https://snapshots.linaro.org/ldcg/python-cache/`
`pip3 install tensorflow-2.7.0-cp39-cp39-linux_aarch64.whl`

The index URL is to include tensorflow-io which is required as per the issue here:
https://github.com/tensorflow/io/issues/1441

and it grabs that wheel from:
https://snapshots.linaro.org/ldcg/python-cache/

Hopefully, in time, the proper tensorflow wheel is just added to the Bullseye repo. I did try compiling Tensorflow for 
32 bit RPi OS, but it was a nightmare, and I don't think was going to work - the prior OS Buster also did not have the
required PostgreSQL-dev-13 installation in its repo that is required.

##### eSpeak setup

The Bot Engine is designed to use eSpeak as its native TTS; but there is no reason why this cannot be changed to use 
something else.

###### Windows

Download the .msi installer from: https://github.com/espeak-ng/espeak-ng/releases

Add the installation location to your PATH, eg:

`C:\Program Files\eSpeak NG`

###### Linux (x86-64/ARM)

Should be as simple as:

`sudo apt-get install espeak-ng python3-gst-1.0 espeak-ng-data libespeak-ng-dev`

Then setting the voice:

`espeak-ng -v gmw/en`

and testing with:

`espeak-ng "Hello, how are you?" 2>/dev/null`

Check the User Guide for more information on both of the
above: https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md

##### Setting up the Chatbot and Sentiment models

###### Windows/Linux x86-64

Under the Chatbot_8/build directory again.

Windows - should be able to run:

`build_postgresql_container.cmd`

Input any name for the container, input password as 'chatbot' and port as '5432' if the script asks for them.

Linux - should be able to run:

`build_postgresql_container_linux.sh <container_name> <postgres password (chatbot)> <port (5432)>`

###### Raspberry Pi OS 64-bit ARM/Linux General

First ensure you have a PostgreSQL server setup as per the instructions of the 
Chatbot - https://github.com/LordofBone/Chatbot_8#docker-postgresql-installation - for Linux on Raspberry Pi due to the 
fact that the 64 bit OS is required for Tensorflow you will need to use the:

`build_postgresql_container_linux.sh <container_name> <postgres password (chatbot)> <port (5432)>`

Script, rather than the '_pi' one, as the 64 bit OS has a different repo and doesn't require the workaround present
there.

Also install Portainer using:

`portainer_build_linux.sh`

Which will allow you go to localhost:9000 to administer Docker containers easily within Linux.

###### Running the training

Ensure the Docker container from above is running.

Drop a training file into the Chatbot data path (the same instructions for the training file for the chatbot apply
here - https://github.com/LordofBone/Chatbot_8#training-the-bot):

`Chatbot_8/data/training/`

Run:

`python train_ai.py`

This should also install the submodule 'Chatbot_8' if it's not already using the command:

`pip install -e Chatbot_8/`

If you preferred to run this yourself, you can. This is a bit of a hacky way to get around the weird directory 
structure stuff you have to deal with in Python; I find that if I just import stuff from the Chatbot_8 directory 
it has trouble finding the /data/training folders and stuff as Python likes to be relative to the file it's initially 
being run from.

If anyone knows a better way around this than using the above pip install method, let me know.

After that it will then train the bot from the training data supplied, and also train a markovify model for the bot 
and put it under Chatbot_8/models/markovify/bot_1.

It will also run the sentiment training, which will then download a set of various NLTK + Tensorflow datasets and models
and the train on them.

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

Here audio can be switched on or off and the varying levels of the Chat bots pitch and cadence can be adjusted.