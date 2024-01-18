import re
# import sys
# TODO: doesn't work! sys.path.append('../')
#  https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
# from speech2text.pattern ........
# from playsound import playsound


class PatternRecognizerText2Speech():

    def recognize_number(input_string):
        # Define a regular expression pattern for matching numbers one to four
        pattern = re.compile(r'\b(one|two|three|four|1|2|3|4)\b', re.IGNORECASE)

        # Find all matches in the input string
        matches = pattern.findall(input_string)

        # Define a dictionary to map words to numbers
        number_mapping = {'one': 1, 'two': 2, 'three': 3, 'four': 4,
                          '1': 1, '2': 2, '3': 3, '4': 4}

        # Initialize the result variable
        result = []

        # Append the corresponding numbers for each match
        # for match in matches:
        #     result.append(number_mapping[match.lower()])

        if len(matches) > 1:
            # TODO: provide an audio from gtts instead of text
            raise Exception('Something went wrong. More than one number was found.')
        else:
            return number_mapping[matches[0].lower()]


if __name__ == '__main__':
    #speech_recognizer = SpeechRecognizer() # how to import

    user_input = input('please, give me the number of measurements you want to take\n')
    print(PatternRecognizerText2Speech.recognize_number(user_input))


    #playsound('../text2speech/generated_utterances/google_tts/please_tell_me_the_number_of_measureme.mp3')
    #user_voice_input = speech_recognizer.speech2text()
    #print(f'here is your input: {user_voice_input}')
    #recognized_number = recognize_number(user_voice_input)
    #print(recognized_number)

