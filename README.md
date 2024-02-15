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

**Hypothesis testing:**

Let's consider a scenario where you're sensitive to caffeine but unsure about the amount of coffee that's safe for you. Utilizing speech4tracking can offer a straightforward approach to test this. Here's how:

1. Begin by taking a series of baseline measurements of your blood pressure and heart rate over at least 30 days without consuming any coffee. Ensure consistency in the timing of these measurements each day.


2. Next, introduce coffee into your daily routine for the following 30 days. For instance, you might choose to consume two cups of espresso per day. Again, maintain consistency in the timing of your coffee consumption.


3. During this coffee consumption period, continue measuring your blood pressure and heart rate at the same time intervals as during the baseline period.


4. After completing both phases (30 days without coffee and 30 days with coffee), you'll have gathered a total of 60 days' worth of data.


5. Utilize statistical hypothesis testing to analyze whether there's a significant difference in your blood pressure and heart rate between the coffee consumption period and the baseline period.


6. By conducting this analysis, you'll be able to determine whether caffeine intake has an observable effect on your blood pressure and heart rate.

This systematic approach can provide valuable insights into how caffeine impacts your body, helping you make informed decisions about your coffee consumption.


Similarly, you can also use this method to assess the impact of various factors such as engaging in sports activities, taking medications, and so forth.

**Medical Recommendation:**

The "Hochdruckliga" (High Blood Pressure League) [recommends](https://www.hochdruckliga.de/fileadmin/downloads/presse/pressemeldungen/2019/WHT_Hintergrund_Blutdruckmessen_in_5_Schritten.pdf) 
taking blood pressure readings three times consecutively 
for accuracy. The measurements must be averaged, data be timestamped and stored 
in a database. We believe that leveraging speech recognition technology can significantly streamline these tasks. 

# How to install

_The app was developed under Python 3.10_

**On Windows:**

- [Download and install Python](https://www.python.org/downloads/release/python-31011/) (if not already installed )


- [Download and install Anaconda](https://www.anaconda.com/download) (or use a Python virtual environment)


- [Download and install git](https://git-scm.com/downloads) (if not already installed)


- Open `Anaconda Prompt` on your PC


- Create a new environment by typing: `conda create --name s4t` and then activate it `conda activate s4t`


- Install pipreqs: `pip install pipreqs`


- Navigate to a directory, where you want to store the app and then get it by typing: `git clone https://github.com/bourgeois-radical/speech4tracking`


- Go to the root folder of the project (`directory_you_have_chosen/speech4tracking`) and install the required dependencies using: `pip install -r requirements.txt`


- Finally, run the app: `python main.py`


- Enjoy!


**Next time, simply open `Anaconda Promt`, activate the environment `conda activate s4t` and run the app using `python main.py`**


# How to use
_When you first launch the app, you'll be prompted to choose between two interfaces:_

#### 1. Text interface:

The text interface is faster and more stable. Speech input is limited to blood pressure and heart rate inputs.

#### 2. Audio interface:

With the audio interface, you interact solely via voice (except for menu choices). 
While using the audio interface may take more time for input, it can be more enjoyable, 
especially for first-time users. However, please note that it may still encounter technical issues 
(refer to the "Under the Hood. Weak Points" section below).

# Under the Hood. Weak Points

### Text Interface:

We implemented Google's ASR (Automatic Speech Recognition) system using the 
[SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library. 
Although precise details about the underlying model are not readily available, 
we speculate that the paper 
[Google USM: Scaling Automatic Speech Recognition Beyond 100 Languages](https://arxiv.org/abs/2303.01037) 
might shed some light on this aspect.

The text interface doesn't exhibit any significant shortcomings that could impede the app's usability.

### Audio Interface:

For the app's responses, we employed Google's TTS (Text-to-Speech) model via the 
[gTTS](https://pypi.org/project/gTTS/) library. 
Unfortunately, to our knowledge, there is no available paper detailing the Google TTS model.

There are some issues with the audio interface:

- In the current version of the app, instructions are always provided audibly. 
Unlike the text interface where you might opt not to read them, in the audio interface,
you'll always hear them pronounced by the app, which may require additional waiting time (see the "TODO-lists" section below).
- When the app prompts, "Have you completed your measurement? 
Are you ready to input it? Please respond with 'yes' or 'no'," 
you must provide an immediate response. This requirement may be inconvenient 
if you're still in the process of measuring your blood pressure 
(see the "TODO-lists" section below).

# TODO-lists (for contributors)

Please feel free to contribute to the source code and these TODO-lists.

<details>
  <summary><b><i>For both interfaces (user_interface_base.py):</i></b></summary>
<ul>
  <li>Implement the second menu choice: adding measurements via keyboard</li>
  <li>Implement the third menu choice: adding measurements via .wav files</li>
  <li>Implement the fourth menu choice: print n last records filtered by date or effect (activity, substance etc.)</li>
</ul>
</details>


<details>
  <summary><b><i>Text interface (cl_user_interface.py):</i></b></summary>
<ul>
    <li>Implement a stable method for hypothesis testing (for each feature: systolic, diastolic, heart rates)</li>
    <li>Add a time frame / accepted time gap for hypothesis testing: if a user takes 'pure' measurements daily at 10 a.m.,
then they should be allowed to take affected measurements within a reasonable time frame (e.g., from 9 to 11 a.m.). If this condition is not satisfied, the app should warn that the t-test results may become untrustworthy</li>
    <li>Allow the user to specify data stamps manually</li>
    <li>Support audio input in other languages (German, Russian, Japanese etc.)</li>
    <li>Add more patterns for voice input (like "132 over 77" etc.)</li>
    <li>Enable the user to provide their age, allowing the app to automatically adjust parameters such as F0, shimmer, and jitter for more accurate recognition, especially useful for elderly people</li>
    <li>Allow the user to provide a few supervised inputs (speech and its text target) so that the ASR model can be fine-tuned for each user (potentially achievable with Whisper)</li>
    <li>Provide a user interface with fewer instructions for users who have become accustomed to the app</li>
    <li>Implement automatic generation of reports for doctors (in PDF or another format)</li>
    <li>Introduce unit tests for each method, not only for pattern recognizers. For example, if there is no systolic, diastolic, or heart rate (a user simply didn't pronounce any of them), then `None` will be returned, and NumPy's mean cannot be calculated with `None`. This error must be fixed. More unit tests are needed!</li>
</ul>
</details>


<details>
  <summary><b><i>Audio interface (audio_user_interface.py):</i></b></summary>
<ul>
  <li>Provide an interface where app-generated utterances have fewer instructions for users who have already become accustomed to the app</li>
  <li>Modify the prompt "Have you done your measurement? Are you ready to input it? Tell me yes or no". After that, the user's response must not follow immediately (as it does now). The user may still be measuring their blood pressure. Additionally, fix any errors occurring in the case of a negative ('no') response</li>
<li>Implement menu choice via voice input</li>
  <li>Add utterances for different numbers of measurements:
    <ul>
    <li>"Have you done your first/second/third measurement?"</li>
    <li>"Here are the average rates from one/two/three measurements..."</li>
    </ul>
</li>
</ul>
</details>


# Rights claim
This is a non-profit open-source project. Feel free to contribute. As of February 14, 2024, all code belongs to
Andrius Rumša (GitHub account: `bourgeois-radical`)


