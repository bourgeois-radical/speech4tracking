# Speech4Tracking - Voice-Enabled Blood Pressure and Heart Rate Tracking

**Introduction:**

Welcome to the Speech4Tracking project repository! We are developing an application that allows 
individuals to effortlessly input systolic and diastolic blood pressure readings, 
along with heart rates from their blood pressure monitors, using voice commands. This concept aims to simplify 
and expedite a process that typically involves multiple manual steps. Moreover, the app empowers 
users to conduct hypothesis testing. This is supposed to help them assess the impact of dietary supplements 
(e.g. Coffeine, Creatine, Ashwagandha etc.), specific activities (e.g. sport, work, amount of sleeping time etc.), 
medications (e.g. antihypertensives etc.) on their blood pressure and heart rates.
This functionality is especially valuable for individuals sensitive to changes in blood pressure and who are curious about,
which activities, dietary supplements or medications are effecting it. 

## Why Speech4Tracking?

**A Novel Approach:**

As of our research, we haven't identified any existing applications that offer the convenience of voice-input for 
blood pressure and heart rate monitoring with hypothesis testing. This approach promises to make health tracking more accessible 
and efficient for users. Given that a generic blood pressure monitor lacks internet connectivity, users must 
find a way to transfer their readings to a computer. With speech input, you can simply 
vocalize the readings displayed on the monitor after each measurement, eliminating the 
need to memorize and manually input the numbers. Moreover, the posture required for 
blood pressure measurement may be inconvenient for using a keyboard, making voice 
input particularly advantageous in such scenarios.

**Medical Recommendation:**

The "Hochdruckliga" (High Blood Pressure League) recommends taking blood pressure readings three times consecutively 
for accuracy. The measurements must be averaged, data be timestamped and stored 
in a database. We believe that leveraging speech recognition technology can significantly streamline these tasks. 

# How to install

_The app was developed under Python 3.10_

**On Windows:**

- [Download and install Python](https://www.python.org/downloads/release/python-31011/) (if not installed already)


- [Download and install Anaconda](https://www.anaconda.com/download) (or feel free to use python virtual environment)


- [Download and install git](https://git-scm.com/downloads) (if not installed already)


- Open `Anaconda Prompt` installed on your PC


- Create a new environment by typing in: `conda create --name s4t` and then activate it `conda activate s4t`


- Install pipreqs: `pip install pipreqs`


- Go to a directory, where you want to store the app and then get it by typing in: `git clone https://github.com/bourgeois-radical/speech4tracking`


- Go to the root folder of the project (`directory_you_have_chosen/speech4tracking`) and then run the following command inside the app's folder: `pip install -r requirements.txt`


- Eventually, run the app: `python main.py`


- Enjoy!


**Next time, just open `Anaconda Promt`, activate the environment `conda activate s4t` and run the app `python main.py`**


# How to use
_First message will ask you to choose one of these two interfaces:_

#### 1. Text interface:

Text interface is more fast and stable. Speech input is intended only for blood pressure and heart rates inputs.

#### 2. Audio interface:

You interact with the app only via voice (except for menu choice). Audio interface takes more time to perform an input. It definitely makes more fun at least for the first time. 
However, it still has some technical issues (see. "Under the Hood. Weak points" section down below).


# Under the Hood. Weak points

### Text interface:

We utilized Google's ASR system using [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library. 
We didn't find any precise information on which model is exactly used under the hood of the API. Nevertheless, we suppose the
paper [Google USM: Scaling Automatic Speech Recognition Beyond 100 Languages](https://arxiv.org/abs/2303.01037) can answer
the question regarding the model being used. 

Text interface doesn't have any shortcomings which can hinder the usage of the app.

### Audio interface:

We utilized Google's TTS model for app's responses, using [gTTS](https://pypi.org/project/gTTS/) library.

There are some issues with the audio interface:

- In the current version of the app the instructions are always given, whereas in the text interface you may just don't read them.
Here, in audio interface, they will always be pronounced by the app, and you will have to wait (see. "TODO-lists" section down below)
- When the app asks "Have you done your measurement? Are you ready to input it? Tell me yes or no" you must answer immediately,
which doesn't make much sense, since you may be still measuring your blood pressure (see. "TODO-lists" section down below)

# TODO-lists (for contributors)

<details>
  <summary><b><i>Text interface:</i></b></summary>
<ul>
  <li>The list is to be enhanced...</li>
</ul>
</details>


<details>
  <summary><b><i>Audio interface:</i></b></summary>
<ul>
  <li>Provide an interface, where app's generated utterances have fewer instructions 
(for the case, if the user has already gotten used to the app)</li>
  <li>"Have you done your measurement? Are you ready to input it? Tell me yes or no". After that, the users' response must not 
follow immediately (as it is now). The user can still be measuring his blood pressure. Additionally, 
an error occurring in the case of negative ('no') response must be fixed</li>
<li>Menu choice must be done via voice input</li>
  <li>The list is to be enhanced...</li>
</ul>
</details>


# Rights claim
This is a non-profit open-source project. Feel free to contribute. As of February 14, 2024, all code belongs to
Andrius Rumša (github: `bourgeois-radical`)


