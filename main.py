import os
import numpy as np
from modules.speech2text.speech_input import SpeechRecognizer
from modules.speech2text.pattern_recognizer import PatternRecognizerSpeech2Text
from modules.text2speech.pattern_recognizer import PatternRecognizerText2Speech
from modules.text2speech.tts_current_measurement import save_current_voice_input_as_mp3
from databases.bp_hr_aff_database import BpHrAffectDatabase
from modules.hypothesis_testing.t_test import TTest
from enum import Enum
from playsound import playsound
from typing import Sequence, Union
from pathlib import Path

# def kukaracha (before_while, before_if, inside_if, inside_elif, inside_else):
#         before_while
#     While True:
#             before_if
#         if:
#             inside_if     USE MATCH-CASE
#         elif:
#             inside_elif
#         else:
#             inside_else


INTERFACE_OPTIONS_DICT = {
    1: 'the app responds you via text',
    2: 'the app responds you via speech'
}


def choose_interface_type(interface_options: dict = INTERFACE_OPTIONS_DICT) -> Union[int, None]:
    """

    Returns
    -------

    """

    print('choose the interface by typing in the number 1 or 2 \n'
          'note:\n'
          '1: the app responds you via text\n'
          '2: the app responds you via speech\n')

    while True:
        try:
            interface_type = int(input())

        except ValueError:
            print(f'invalid input! it must be an integer corresponding to a valid interface option.\n'
                  'please, type in your choice once again\n')
        else:
            if interface_type in interface_options.keys():
                return interface_type
            else:
                print('the integer you typed in does not correspond to any valid interface option.\n'
                      'please, type in your choice once again\n')

                # return
                # with return: the menu is printed once again if the input was wrong
                # without return: the menu is printed only once since we loop inside this function


def print_menu():
    """

    Returns
    -------

    """
    print("""\nwhat are we gonna do?
    1. add a record (speech2text)
    2. add a record (keyboard)
    3. add a record(-s) (.wav file)
    4. print n last records
    5. perform a hypothesis test
    6. exit
        """)

    return


MENU_OPTIONS_DICT = {
    1: 'add a record (speech2text)',
    2: 'add a record (keyboard)',
    3: 'add a record(-s) (.wav file)',
    4: 'print n last records',
    5: 'perform a hypothesis test',
    6: 'exit'
}


def handle_user_menu_response(menu_options: dict = MENU_OPTIONS_DICT) -> Union[int, None]:
    while True:
        try:
            user_response = int(input())
        except ValueError:
            print(f'invalid input! it must be an integer corresponding to a valid menu option.\n'
                  'please, type in your choice once again')
        else:
            if user_response in menu_options.keys():
                return user_response
            else:
                print('the integer you typed in does not correspond to any valid menu option.\n'
                      'please, type in your choice once again')

            # return
            # with return: the menu is printed once again if the input was wrong
            # without return: the menu is printed only once since we loop inside this function


ALLOWED_NUMBER_OF_MEASUREMENTS_LIST = [1, 2, 3]


def input_number_of_measurements(allowed_number_of_measurements: list = ALLOWED_NUMBER_OF_MEASUREMENTS_LIST):
    print('please, type in the number of measurements you want to take:')

    while True:
        user_response = input()
        if user_response == 'quit':
            return 'quit_entering_the_number_of_measurements'
        else:
            try:
                user_response = int(user_response)
                # if user_response == 478:
                #     break
            except ValueError:
                print(f'invalid input! it must be a natural number.\n'
                      'please, type in the number of measurements you want to take once again')
            else:
                if user_response in allowed_number_of_measurements:
                    return user_response
                else:
                    print("the input you provided does not correspond to allowed number of measurements.\n"
                          "you can take 1, 2 or 3 measurements\n"
                          "you can type in your choice once again or type in 'quit' to quit")
                    # TODO: allow user to leave typing in the number of measurements


class MenuChoice(Enum):
    """ """
    VOICE_INPUT = 1
    KEYBOARD_INPUT = 2
    IMPORT_FROM_WAV = 3
    PRINT_N_LAST_RECORDS = 4
    PERFORM_HYPOTHESIS_TEST = 5
    EXIT = 6

    # TODO: finish it and then use in if else statements instead of == 1, 2, 3 etc.


class AppResponseInterface(Enum):
    TEXT = 1  # the app responds user via text
    SPEECH = 2  # the app responds via automatically generated speech (TTS)


def print_n_last_records():
    # print('here are your last records:')
    raise NotImplementedError('Sorry, last-records-printing is not available at the moment. '
                              'We are working on implementing this feature and appreciate your understanding.')


def keybord_input():
    # print('please, type in your record')
    raise NotImplementedError('Sorry, keyboard input is not available at the moment. We are working on '
                              'implementing this feature and appreciate your understanding.')


def import_from_wav():
    # print('provide the names of the .wav files')
    raise NotImplementedError('Sorry, import from wav-files is not available at the moment. '
                              'We are working on implementing this feature and appreciate your understanding.')


def iterative_input_of_measurements(number_of_measurements: int, speech_recognizer_instance: SpeechRecognizer) \
        -> Sequence[str]:
    """

    Parameters
    ----------
    number_of_measurements : int
        Number of measurements a user wants to make
    speech_recognizer_instance : SpeechRecognizer

    Returns
    -------
     all_measurements : Sequence[str]
        Voice inputs of a user in form of python string

    """

    all_measurements = []
    for measurement in range(number_of_measurements):
        # kukaracha
        while True:
            # TODO: suggestion to take a break between measurements

            #  measurement + 1 so that we show user his measurements starting from 1, not from 0
            is_measurement_done = input(
                f'\nhave you done your {measurement + 1} measurement? are you ready to input it? [Y/n] ')
            if is_measurement_done == 'Y':  # TODO: Добавить yes, y etc. через Enum
                print('we are listening to you...')
                # FIXME: speech_recognition.exceptions.UnknownValueError if there is no speech input
                #  solution: try except

                # TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”)
                # TODO: try to input in other languages
                user_voice_input = speech_recognizer_instance.speech2text()
                print(f'measurement #{measurement + 1}: {user_voice_input}')

                # check values before adding to the overall list
                while True:
                    correctly_recognized = input('\nwas the measurement recognized correctly? [Y/n] ')
                    if correctly_recognized == 'Y':
                        all_measurements.append(user_voice_input)
                        break
                    elif correctly_recognized == 'n':
                        # TODO: manual correction
                        print("\nlet's try once again!")
                        print('we are listening to you...')
                        user_voice_input = speech_recognizer_instance.speech2text()
                        print(f'measurement #{measurement + 1}: {user_voice_input}')
                    else:  # correctly_recognized != 'Y' and correctly_recognized != 'n':
                        print('\nplease, type in Y or n')

                # if a measurement was successfully recognized we quit the first 'while' loop
                # and go to the next iteration/measurement inside 'for' loop
                break
            elif is_measurement_done == 'n':
                print('\nnot a problem! we are waiting for you :)')
            elif is_measurement_done != 'Y' and is_measurement_done != 'n':
                print('\nplease, type in Y or n')

    return all_measurements


def calculate_average_rates(all_measurements: Sequence[str]) -> Sequence[int]:
    """After having collected all measurements (str) in one list, we must find the rates (int) of interest.

    Parameters
    ----------
    number_of_measurements : int
    all_measurements : Sequence[str]

    Returns
    -------
    systolic : int
    diastolic : int
    heart_rate : int

    """
    pattern_recognizer = PatternRecognizerSpeech2Text()
    all_measurements = pattern_recognizer.blood_pressure_heart_rate_from_voice(
        recognized_voice_inputs=all_measurements)
    print(all_measurements)
    # count the mean from n (the number is provided by user) measurements
    all_measurements = np.mean(np.array(all_measurements), axis=1)
    systolic = all_measurements[0]
    diastolic = all_measurements[1]
    heart_rate = all_measurements[2]
    # TODO: change allowed_number_of_measurements to len(all_measurements)
    print(f'\nhere are the average rates from {len(all_measurements)} measurement(-s): \nsys: {systolic}'
          f'\ndia: {diastolic} \nhr: {heart_rate}')

    return systolic, diastolic, heart_rate


def add_affect() -> str:
    """This function helps to input an affect. Affect is something what can potentially influence blood pressure rates.

    Returns
    -------

    affect : str
        Substance, activity etc.

    """

    while True:
        affect_presence_yes_or_no = input(
            '\ndo you do any activities (gym, work etc.), '
            'take any medication or consume any substances (e.g. antihypertensives, coffee etc.)\n'
            'the effects of which you want to control regarding your blood pressure? [Y/n] ')

        if affect_presence_yes_or_no == 'Y':

            affect = input('\nwhat can potentially affect your rates? please, type in what it is\n')
            # remove spaces at the beginning and at the end of the string:
            affect = affect.strip()
            if len(affect) > 0:
                correct_affect_input = input(f"\nis your input correct? '{affect}' [Y/n] ")
                if correct_affect_input == 'Y':
                    print('\nnice!')
                    break
                elif correct_affect_input == 'n':
                    print("\nlet's try once again!")
                elif correct_affect_input != 'Y' and correct_affect_input != 'n':
                    print('\nplease, type in Y or n')

        elif affect_presence_yes_or_no == 'n':
            affect = 'no_affect'
            print("\nroger that! it will be marked as 'no_affect'")
            break
        elif affect_presence_yes_or_no != 'Y' and affect_presence_yes_or_no != 'n':
            print('\nplease, type in Y or n')

    return affect


def add_measurements_to_db(systolic, diastolic, heart_rate, affect):
    """

    Returns
    -------

    """
    bp_hr_aff_db = BpHrAffectDatabase()
    connection = bp_hr_aff_db.create_connection(db_path='./databases/test.db')

    if connection is not None:
        bp_hr_aff_db.create_table(connection=connection)
    else:
        print('error! cannot create the databases connection')

    # add measurements to the db
    bp_hr_aff_db.insert_row(connection=connection, systolic=systolic, diastolic=diastolic,
                            heart_rate=heart_rate,
                            affect=affect)

    # close connection to the db
    bp_hr_aff_db.close_connection(connection=connection)

    print('the measurement has been successfully added to database!')
    return  # actually, returns None. It's a procedure in normal programming languages


def perform_demo_hypothesis_test():
    """Creates a database if it doesn't exist already, uploads fake measurements (40 with coffee and 40 without),
    then performs a hypothesis testing for systolic blood pressure rates."""

    print('the functionality of this menu subsection is under development.\n'
          'please, enjoy the demo :)\n\n'
          'experimental conditions:\n'
          '40 measurements without coffee\n'
          '40 measurements with coffee\n'
          'type of test: paired t-test\n'
          )
    # TODO: hypothesis test
    #  -1: we need two databases: one for current experiment, one for all?
    #  + 0. create a fake db (30 pure, 30 coffee) +
    #  1. write a query which creates two samples (retrieve all pure and with affect from current experience db)
    #  2. perform a t-test (3 tests: sys, dia, hr)

    demo_bp_hr_aff_db = BpHrAffectDatabase()
    demo_connection = demo_bp_hr_aff_db.create_demo_connection(db_path='./databases/demo.db')
    # demo_bp_hr_aff_db.initialize_fake_measurements(demo_connection)

    # retrieve two paired samples for diastolic
    sys_rows_affected = demo_bp_hr_aff_db.retrieve_measurements_for_demo_test(
        connection=demo_connection,
        rate_of_interest='sys',
        affected_by='coffee')

    sys_rows_not_affected = demo_bp_hr_aff_db.retrieve_measurements_for_demo_test(
        connection=demo_connection,
        rate_of_interest='sys',
        affected_by='no_affect')

    # perform a hypothesis test
    paired_t_test = TTest()
    # TODO: t_stat minus sign tells us about the direction
    #  (grater [coffee] - less = +) or (less - grater [coffee] = -)
    paired_t_test.sys_paired_t_test(not_affected=sys_rows_not_affected,
                                    affected=sys_rows_affected,
                                    affected_by='coffee')
    # TODO: create a separate function "distribution_check"
    # check distribution
    # sns.set_theme(style="darkgrid")
    # sys_rows_affected_df = pd.DataFrame(sys_rows_affected)
    # sys_rows_not_affected_df = pd.DataFrame(sys_rows_not_affected, columns=['sys_not_affected'])
    # print(sys_rows_not_affected_df.head())
    # sns.displot(
    #     sys_rows_not_affected_df, x='sys_not_affected',
    #     binwidth=1, height=3  # facet_kws=dict(margin_titles=True),
    # )
    # plt.show()

    return  # actually, returns None. It's a procedure in normal programming languages


# speech modules:

def input_number_of_measurements_speech_based(speech_recognizer_instance: SpeechRecognizer,
                                              allowed_number_of_measurements: list = ALLOWED_NUMBER_OF_MEASUREMENTS_LIST):
    # print('please, type in the number of measurements the user wanna take
    playsound(
        'modules/text2speech/generated_utterances/google_tts/please_tell_me_the_number_of_measureme.mp3')

    while True:
        number_of_measurements_user_voice_input = speech_recognizer_instance.speech2text()
        print(number_of_measurements_user_voice_input)

        try:
            n_measurements = PatternRecognizerText2Speech.recognize_number(
                number_of_measurements_user_voice_input)

        except ValueError:
            # TODO: is it ok to catch an Exception?
            # the number of measurements must be a natural number. Restart the app. Otherwise, good bye!
            playsound(
                'modules/text2speech/generated_utterances/google_tts/the_number_of_measurements_must_be_a_natural_number_Restart.mp3')

        else:
            if n_measurements in allowed_number_of_measurements:
                return n_measurements

    playsound(
        'modules/text2speech/generated_utterances/google_tts/please_prepare_your_blood_pressure_monitor_and_give_your.mp3')
    # print("\n'systolic #number#, diastolic #number#, heart rate #number#'")
    playsound(
        'modules/text2speech/generated_utterances/google_tts/pronounce_systolic_and_then_provide_a_number.mp3')

    return n_measurements


def iterative_input_of_measurements_speech_based(number_of_measurements: int,
                                                 speech_recognizer_instance: SpeechRecognizer):
    """

    Parameters
    ----------
    number_of_measurements
    speech_recognizer_instance

    Returns
    -------

    """

    def block_of_generated_utterances_prepare_blood_pressure_monitor_and_pronounce_measurements():
        playsound(
            'modules/text2speech/generated_utterances/google_tts/please_prepare_your_blood_pressure_monitor_and_give_your.mp3')
        # print("\n'systolic #number#, diastolic #number#, heart rate #number#'")
        playsound(
            'modules/text2speech/generated_utterances/google_tts/pronounce_systolic_and_then_provide_a_number.mp3')

        return

    def user_input_of_measurements_and_check_their_correctness() -> list:

        all_measurements = []
        # TODO: make it possible to input more than one measurement
        for measurement in range(number_of_measurements):
            # kukaracha
            while True:
                # TODO: suggestion to take a break between measurements
                # TODO: !!!provide more precise utterances: have you done your first/second/third/forth measurement!!!!
                playsound(
                    'modules/text2speech/generated_utterances/google_tts/have_you_done_your_measurement_are_you_ready_to_inp.mp3')
                is_ready_to_input = speech_recognizer_instance.speech2text()
                is_ready_to_input = PatternRecognizerText2Speech.recognize_yes_or_no(
                    is_ready_to_input)

                if is_ready_to_input is True:  # TODO: Add yes, y etc. with Enum???
                    playsound('modules/text2speech/generated_utterances/google_tts/we_are_listening.mp3')
                    # FIXME: speech_recognition.exceptions.UnknownValueError if there is no speech input
                    # TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”)
                    # TODO: try to input in other languages (it seems, it doesn't work)

                    # TODO: pattern! define a function for generation of current measurements
                    user_voice_input = speech_recognizer_instance.speech2text()
                    save_current_voice_input_as_mp3(user_voice_input)
                    playsound('modules/text2speech/generated_utterances/current_measurement.mp3')

                    #  immediately delete the generated audio-file
                    if os.path.exists('modules/text2speech/generated_utterances/current_measurement.mp3'):
                        os.remove('modules/text2speech/generated_utterances/current_measurement.mp3')
                    else:
                        print('The file does not exist')
                    # TODO: end of the pattern

                    # check values before adding to the overall list
                    while True:
                        playsound(
                            'modules/text2speech/generated_utterances/google_tts/was_the_measurement_recognized_correctl.mp3')
                        is_correctly_recognized = speech_recognizer_instance.speech2text()
                        is_correctly_recognized = PatternRecognizerText2Speech.recognize_yes_or_no(
                            is_correctly_recognized)
                        if is_correctly_recognized is True:  # TODO: change to MATCH-CASE + use ENUM
                            all_measurements.append(user_voice_input)
                            break
                        elif is_correctly_recognized is False:
                            # TODO: manual correction
                            playsound(
                                'modules/text2speech/generated_utterances/google_tts/lets_try_once.mp3')
                            break # nested loop

                        else:
                            playsound(
                                'modules/text2speech/generated_utterances/google_tts/I_didnt_get_you_please_just_s.mp3')
                # else:
                    # TODO: user is not ready to input
                break # main while loop and go to the for loop

        return all_measurements

    match number_of_measurements:

        case 1:
            playsound('modules/text2speech/generated_utterances/google_tts/ok_we_are_ready_to_take_one.mp3')
            # TODO: ask the user, whether he needs these two instructions down below
            block_of_generated_utterances_prepare_blood_pressure_monitor_and_pronounce_measurements()
            all_measurements = user_input_of_measurements_and_check_their_correctness()
            return all_measurements

        case 2:
            playsound('modules/text2speech/generated_utterances/google_tts/ok_we_are_ready_to_take_two.mp3')
            # TODO: ask the user, whether he needs these two instructions down below
            block_of_generated_utterances_prepare_blood_pressure_monitor_and_pronounce_measurements()
            all_measurements = user_input_of_measurements_and_check_their_correctness()
            return all_measurements

        case 3:
            playsound('modules/text2speech/generated_utterances/google_tts/ok_we_are_ready_to_take_three.mp3')
            # TODO: ask the user, whether he needs these two instructions down below
            block_of_generated_utterances_prepare_blood_pressure_monitor_and_pronounce_measurements()
            all_measurements = user_input_of_measurements_and_check_their_correctness()
            return all_measurements

        case 4:
            playsound('modules/text2speech/generated_utterances/google_tts/ok_we_are_ready_to_take_four.mp3')
            # TODO: ask the user, whether he needs these two instructions down below
            block_of_generated_utterances_prepare_blood_pressure_monitor_and_pronounce_measurements()
            all_measurements = user_input_of_measurements_and_check_their_correctness()
            return all_measurements


def calculate_average_rates_speech_based(all_measurements: Sequence[str]) -> Sequence[int]:
    """After having collected all measurements (str) in one list, we must find the rates (int) of interest.

    Parameters
    ----------
    number_of_measurements : int
    all_measurements : Sequence[str]

    Returns
    -------
    systolic : int
    diastolic : int
    heart_rate : int

    """
    pattern_recognizer = PatternRecognizerSpeech2Text()
    all_measurements = pattern_recognizer.blood_pressure_heart_rate_from_voice(
        recognized_voice_inputs=all_measurements)
    # count the mean from n (the number is provided by user) measurements
    all_measurements = np.mean(np.array(all_measurements), axis=1)
    systolic = all_measurements[0]
    diastolic = all_measurements[1]
    heart_rate = all_measurements[2]

    average_rates = f'here are the average rates from {len(all_measurements)} measurement(-s): systolic: {systolic} diastolic: {diastolic} heart rate: {heart_rate}'
    # TODO: add utterance: 'here are your average rates'
    save_current_voice_input_as_mp3(average_rates)
    # TODO: rename 'current_measurement' to 'current_input' or whatever. Use an f string with a variable so that one can refactor it
    playsound('modules/text2speech/generated_utterances/current_measurement.mp3')

    #  immediately delete file after having just created it
    if os.path.exists('modules/text2speech/generated_utterances/current_measurement.mp3'):
        os.remove('modules/text2speech/generated_utterances/current_measurement.mp3')
    else:
        print('The file does not exist')

    return systolic, diastolic, heart_rate


def run_app():
    exit_the_app = False

    while True:  # choosing type of interface: text based or speech based

        interface_type = choose_interface_type()

        if interface_type == AppResponseInterface.TEXT.value:

            # Google ASR API instance
            speech_recognizer = SpeechRecognizer()

            while True:

                print_menu()
                response = handle_user_menu_response()

                match response:
                    case MenuChoice.VOICE_INPUT.value:

                        n_measurements = input_number_of_measurements()

                        if n_measurements == 'quit_entering_the_number_of_measurements':
                            continue

                        all_user_voice_inputs = iterative_input_of_measurements(number_of_measurements=n_measurements,
                                                                                speech_recognizer_instance=speech_recognizer)

                        average_systolic, average_diastolic, average_heart_rate = calculate_average_rates(
                            all_measurements=all_user_voice_inputs)

                        affect = add_affect()

                        add_measurements_to_db(systolic=average_systolic, diastolic=average_diastolic,
                                               heart_rate=average_heart_rate, affect=affect)

                    case MenuChoice.KEYBOARD_INPUT.value:
                        keybord_input()
                    case MenuChoice.IMPORT_FROM_WAV.value:
                        import_from_wav()
                    case MenuChoice.PRINT_N_LAST_RECORDS.value:
                        print_n_last_records()
                    case MenuChoice.PERFORM_HYPOTHESIS_TEST.value:
                        perform_demo_hypothesis_test()
                    case MenuChoice.EXIT.value:
                        exit_the_app = True
                        print('exiting the app...\nit was a pleasure! See you!')
                        break

        if exit_the_app is True:
            break

        elif interface_type == AppResponseInterface.SPEECH.value:

            speech_recognizer = SpeechRecognizer()

            while True:
                # TODO: menu must be in a audio format as well! Generate utterances for menu
                # TODO: check whether the input is integer
                #  if not type(x) is int:
                #     raise TypeError("Only integers are allowed")
                print_menu()
                response = handle_user_menu_response()

                match response:
                    case MenuChoice.VOICE_INPUT.value:
                        n_measurements = input_number_of_measurements_speech_based(
                            speech_recognizer_instance=speech_recognizer
                        )

                        # if n_measurements == 'quit_entering_the_number_of_measurements':
                        #     continue

                        all_user_voice_inputs = iterative_input_of_measurements_speech_based(
                            number_of_measurements=n_measurements,
                            speech_recognizer_instance=speech_recognizer
                        )

                        average_systolic, average_diastolic, average_heart_rate = calculate_average_rates_speech_based(
                            all_measurements=all_user_voice_inputs)

                    case MenuChoice.KEYBOARD_INPUT.value:
                        print('please, type in your record')
                    case MenuChoice.IMPORT_FROM_WAV.value:
                        print('provide the names of the .wav files')
                    case MenuChoice.PRINT_N_LAST_RECORDS.value:
                        print_n_last_records()
                    case MenuChoice.PERFORM_HYPOTHESIS_TEST.value:
                        perform_demo_hypothesis_test()
                    case MenuChoice.EXIT.value:
                        print('it was a pleasure! See you!')
                        break


if __name__ == '__main__':
    run_app()

# TODO: commit all changes to a new branch
