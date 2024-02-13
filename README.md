# Speech4Tracking - Voice-Enabled Blood Pressure and Heart Rate Tracking

**Introduction:**

Welcome to the Speech4Tracking project repository! Our mission is to develop an application that allows 
individuals to effortlessly input systolic and diastolic blood pressure readings, 
along with heart rates from their blood pressure monitors, using voice commands. This concept aims to simplify 
and expedite a process that typically involves multiple manual steps. Moreover, the app empowers 
users to conduct hypothesis testing. This is supposed to help them assess the impact of dietary supplements 
(e.g. Coffeine, Creatine, Ashwagandha etc.), specific activities (e.g. sport, work, amount of sleeping time etc.), 
medications (e.g. antihypertensives etc.) on their blood pressure and heart rates.
This functionality is especially valuable for individuals sensitive to changes in blood pressure and who are curious about,
which activities, dietary supplements or medications can effect it. 

## Why Speech4Tracking?

**A Novel Approach:**

As of our research, we haven't identified any existing applications that offer the convenience of voice-input for 
blood pressure and heart rate monitoring. This approach promises to make health tracking more accessible 
and efficient for users. Given that a generic blood pressure monitor lacks internet connectivity, users must 
find a way to transfer their readings to a computer. With speech input, you can simply 
vocalize the readings displayed on the monitor after each measurement, eliminating the 
need to memorize and manually input the numbers. Moreover, the posture required for 
blood pressure measurement may be inconvenient for using a keyboard, making voice 
input particularly advantageous in such scenarios.

**Medical Recommendation:**
The "Hochdruckliga" (High Blood Pressure League) recommends taking blood pressure readings three times consecutively 
for accuracy. The measurements must be averaged, data be timestamped and stored 
in a database. This process can be time-consuming and error-prone. We believe that leveraging speech
recognition technology can significantly streamline this task. 

# How to use

## On Windows

_The app was developed under Python 3.10_

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


