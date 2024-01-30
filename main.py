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
from typing import Sequence
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


def print_menu():
    print("""\nwhat are we gonna do?
    1. add a record (speech2text)
    2. add a record (keyboard)
    3. add a record(-s) (.wav file)
    4. print n last records
    5. perform a hypothesis test
    6. exit
        """)

def handle_user_menu_response() -> int:

    while True:

        user_response = input()

        try:
            integer_user_response = isinstance(user_response, int)
            return int(user_response)
        except ValueError:
            print('invalid input. Please enter a valid integer.')

        repeat = input('do you want to repeat the input? (Y/n): ').lower()
        if repeat != 'Y':
            print('existing the app.')
            break






class MenuChoice(Enum):
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


def calculate_average_rates(number_of_measuremnts: int, all_measurements: Sequence[str]) -> Sequence[int]:
    """After having collected all measurements (str) in one list, we must find the rates (int) of interest.

    Parameters
    ----------
    number_of_measuremnts : int
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
    print(f'\nhere are the average rates from {number_of_measuremnts} measurement(-s): \nsys: {systolic}'
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

    return 'your record has been successfully added to the database!'


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

    return 'Demo hypothesis test for systolic blood pressure has been successfully performed!'


def run_app():
    while True:  # choosing type of interface: text based or speech based
        interface_type = int(input('choose the interface by typing in the number 1 or 2 \n'
                                   'note:\n'
                                   '1: the app responds you via text\n'
                                   '2: the app responds you via speech\n'))

        if interface_type == AppResponseInterface.TEXT.value:

            # Google ASR API instance
            speech_recognizer = SpeechRecognizer()

            while True:
                print_menu()
                # TODO: check whether the input is integer

                response = handle_user_menu_response()
                print(response)
                # speech2text input
                match response:
                    case MenuChoice.VOICE_INPUT.value:  # TODO: use match/case instead of if/else

                          # TODO: вынести либо до while, но лучше в модуль

                        print('please, type in the number of measurements you wanna take:')
                        # TODO: prevent typing in of characters, str etc. as well. NATURAL NUMBERS ONLY!
                        n_measurements = int(input())
                        if n_measurements <= 0:
                            print(
                                'the number of measurements must be a natural number. Restart the app. Otherwise, good bye!')
                            break
                        print(f'\nok! we are ready to record {n_measurements} measurements')
                        print(f'\nplease prepare your blood pressure monitor and give your input in the following format:')
                        print("\n'systolic #number#, diastolic #number#, heart rate #number#'")

                        all_user_voice_inputs = iterative_input_of_measurements(number_of_measurements=n_measurements,
                                                                                speech_recognizer_instance=speech_recognizer)

                        average_systolic, average_diastolic, average_heart_rate = calculate_average_rates(
                            number_of_measuremnts=n_measurements,
                            all_measurements=all_user_voice_inputs)

                        print('WE ARE HERE')
                        affect = add_affect()

                        print('HI')
                        add_measurements_to_db(systolic=average_systolic, diastolic=average_diastolic,
                                               heart_rate=average_heart_rate, affect=affect)

                        print('WE ARE NOW HERE')
                    case MenuChoice.KEYBOARD_INPUT.value:
                        keybord_input()
                    case MenuChoice.IMPORT_FROM_WAV.value:
                        import_from_wav()
                    case MenuChoice.PRINT_N_LAST_RECORDS.value:
                        print_n_last_records()
                    case MenuChoice.PERFORM_HYPOTHESIS_TEST.value:
                        perform_demo_hypothesis_test()
                    case MenuChoice.EXIT.value:
                        print('it was a pleasure! See you!')
                        break

        elif interface_type == AppResponseInterface.SPEECH.value:

            utterances_src_dir = 'modules/text2speech/generated_utterances/google_tts'

            while True:
                # TODO: menu must be in a audio format as well! Generate utterances for menu
                print_menu()
                # TODO: check whether the input is integer
                #  if not type(x) is int:
                #     raise TypeError("Only integers are allowed")
                response = int(input())
                all_measurements = []

                # speech2text input
                if response == MenuChoice.VOICE_INPUT.value:

                    speech_recognizer = SpeechRecognizer()  # TODO: вынести либо до while, но лучше в модуль

                    # print('please, type in the number of measurements the user wanna take
                    #  TODO: is it a good alternative? str(Path(utterances_src_dir) / Path('please_tell_me_the_number_of_measureme.mp3'))
                    playsound(
                        'modules/text2speech/generated_utterances/google_tts/please_tell_me_the_number_of_measureme.mp3')
                    number_of_measurements_user_voice_input = speech_recognizer.speech2text()
                    # print(number_of_measurements_user_voice_input)
                    n_measurements = PatternRecognizerText2Speech.recognize_number(
                        number_of_measurements_user_voice_input)

                    if n_measurements <= 0:  # TODO: other exceptions as well!
                        # the number of measurements must be a natural number. Restart the app. Otherwise, good bye!
                        playsound(
                            'modules/text2speech/generated_utterances/google_tts/the_number_of_measurements_must_be_a_natural_number_Restart.mp3')
                        break
                    # TODO: match-case: 1, 2, 3, 4 measurements
                    # print(f'\nok! we are ready to record {number_of_measurements} measurements')
                    playsound('modules/text2speech/generated_utterances/google_tts/ok_we_are_ready_to_take_m.mp3')
                    # print(f'\nplease prepare your blood pressure monitor and give your input in the following format:')
                    playsound(
                        'modules/text2speech/generated_utterances/google_tts/please_prepare_your_blood_pressure_monitor_and_give_your.mp3')
                    # print("\n'systolic #number#, diastolic #number#, heart rate #number#'")
                    playsound(
                        'modules/text2speech/generated_utterances/google_tts/pronounce_systolic_and_then_provide_a_number.mp3')

                    # TODO: input/output interation remains inside the main.py module
                    #  but the processing of the inputs must be performed outside the main.py
                    for measurement in range(n_measurements):
                        # kukaracha
                        while True:
                            # TODO: suggestion to take a break between measurements

                            #  measurement + 1 so that we show user his measurements starting from 1, not from 0
                            # ready_for_measurement = input(
                            # f'\nhave you done your {measurement + 1} measurement? are you ready to input it? [Y/n] ')
                            # TODO: provide more precise utterances: have you done your first/second/third/forth measurement
                            playsound(
                                'modules/text2speech/generated_utterances/google_tts/have_you_done_your_measurement_are_you_ready_to_inp.mp3')
                            affect_presence_yes_or_no = speech_recognizer.speech2text()
                            affect_presence_yes_or_no = PatternRecognizerText2Speech.recognize_yes_or_no(
                                affect_presence_yes_or_no)

                            if affect_presence_yes_or_no == 'Y':  # TODO: Добавить yes, y etc. через Enum
                                # print('we are listening to you...')
                                playsound('modules/text2speech/generated_utterances/google_tts/we_are_listening.mp3')
                                # FIXME: speech_recognition.exceptions.UnknownValueError if there is no speech input

                                # TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”)
                                # TODO: try to input in other languages

                                # TODO: pattern_55
                                user_voice_input = speech_recognizer.speech2text()
                                # print(f'measurement #{measurement + 1}: {user_voice_input}')
                                save_current_voice_input_as_mp3(user_voice_input)
                                playsound('modules/text2speech/generated_utterances/current_measurement.mp3')

                                #  immediately delete file after having just created it
                                if os.path.exists('modules/text2speech/generated_utterances/current_measurement.mp3'):
                                    os.remove('modules/text2speech/generated_utterances/current_measurement.mp3')
                                else:
                                    print('The file does not exist')
                                # TODO: pattern_55

                                # check values before adding to the overall list
                                while True:
                                    playsound(
                                        'modules/text2speech/generated_utterances/google_tts/was_the_measurement_recognized_correctl.mp3')
                                    # correctly_recognized = input('\nwas the measurement recognized correctly? [Y/n] ')
                                    correctly_recognized = speech_recognizer.speech2text()
                                    correctly_recognized = PatternRecognizerText2Speech.recognize_yes_or_no(
                                        correctly_recognized)
                                    if correctly_recognized == 'Y':  # TODO: change to MATCH-CASE + use ENUM
                                        all_measurements.append(user_voice_input)
                                        break
                                    elif correctly_recognized == 'n':
                                        # TODO: manual correction
                                        # print("\nlet's try once again!")
                                        playsound(
                                            'modules/text2speech/generated_utterances/google_tts/lets_try_once.mp3')
                                        # print('we are listening to you...')

                                        # TODO: pattern_55
                                        playsound(
                                            'modules/text2speech/generated_utterances/google_tts/we_are_listening.mp3')
                                        user_voice_input = speech_recognizer.speech2text()
                                        # print(f'measurement #{measurement + 1}: {user_voice_input}')
                                        save_current_voice_input_as_mp3(user_voice_input)
                                        playsound('modules/text2speech/generated_utterances/current_measurement.mp3')

                                        #  immediately delete file after having just created it
                                        if os.path.exists(
                                                'modules/text2speech/generated_utterances/current_measurement.mp3'):
                                            os.remove(
                                                'modules/text2speech/generated_utterances/current_measurement.mp3')
                                        else:
                                            print('The file does not exist')
                                        # TODO: patern_55

                                    else:  # correctly_recognized != 'Y' and correctly_recognized != 'n':
                                        # TODO: "I didn't get you! Do u want to repeat an input or leave an app?"
                                        print('\nplease, type in Y or n')
                                        # playsound('modules/text2speech/generated_utterances/google_tts/)

                                # if a measurement was successfully recognized we quit the first 'while' loop
                                # and go to the next iteration/measurement inside 'for' loop
                                break
                            elif affect_presence_yes_or_no == 'n':
                                print('\nnot a problem! we are waiting for you :)')
                                playsound(
                                    'modules/text2speech/generated_utterances/google_tts/not_a_problem_we_are_wait.mp3')
                            elif affect_presence_yes_or_no != 'Y' and affect_presence_yes_or_no != 'n':
                                print('\nplease, type in Y or n')

                    # after having collected all measurements (str) in one list, we must find the rates (int) of interest
                    pattern_recognizer = PatternRecognizerSpeech2Text()
                    all_measurements = pattern_recognizer.blood_pressure_heart_rate_from_voice(
                        recognized_voice_inputs=all_measurements)
                    print(all_measurements)
                    # count the mean from n (the number is provided by user) measurements
                    all_measurements = np.mean(np.array(all_measurements), axis=1)
                    systolic = all_measurements[0]
                    diastolic = all_measurements[1]
                    heart_rate = all_measurements[2]

                    # print(f'\nhere are the average rates from {number_of_measurements} measurement(-s): \nsys: {systolic}'
                    #       f'\ndia: {diastolic} \nhr: {heart_rate}')

                    average_rates = f'here are the average rates from {n_measurements} measurement(-s): systolic: {systolic} diastolic: {diastolic} heart rate: {heart_rate}'
                    save_current_voice_input_as_mp3(average_rates)
                    # TODO: rename 'current_measurement' to 'current_input' or whatever. Use an f string with a variable so that one can refactor it
                    playsound('modules/text2speech/generated_utterances/current_measurement.mp3')

                    #  immediately delete file after having just created it
                    if os.path.exists('modules/text2speech/generated_utterances/current_measurement.mp3'):
                        os.remove('modules/text2speech/generated_utterances/current_measurement.mp3')
                    else:
                        print('The file does not exist')

                    # add an affect
                    while True:
                        # affect_presence = input(
                        #     '\ndo you do any activities (gym, work etc.), '
                        #     'take any medication or consume any substances (e.g. antihypertensives, coffee etc.)\n'
                        #     'the effects of which you want to control regarding your blood pressure? [Y/n] ')
                        playsound(
                            'modules/text2speech/generated_utterances/google_tts/do_you_do_any_activities_gym_work_etc_take_any_medication.mp3')
                        affect_presence_yes_or_no = speech_recognizer.speech2text()
                        affect_presence_yes_or_no = PatternRecognizerText2Speech.recognize_yes_or_no(
                            affect_presence_yes_or_no)
                        if affect_presence_yes_or_no == 'Y':

                            # affect = input('\nwhich affect do you take then? please, typy in: ')
                            playsound(
                                'modules/text2speech/generated_utterances/google_tts/what_can_potentially_affect_your_rates_pleas.mp3')
                            affect = speech_recognizer.speech2text()
                            # print(f'measurement #{measurement + 1}: {user_voice_input}')
                            save_current_voice_input_as_mp3(affect)

                            # remove spaces at the beginning and at the end of the string:
                            affect = affect.strip()
                            if len(affect) > 0:
                                # correct_affect_input = input(f"\nis your input correct? '{affect}' [Y/n] ")
                                playsound(
                                    'modules/text2speech/generated_utterances/google_tts/is_your_input_correct.mp3')
                                playsound('modules/text2speech/generated_utterances/current_measurement.mp3')
                                #  immediately delete file after having just created it
                                if os.path.exists('modules/text2speech/generated_utterances/current_measurement.mp3'):
                                    os.remove('modules/text2speech/generated_utterances/current_measurement.mp3')
                                else:
                                    print('The file does not exist')

                                correct_affect_input = speech_recognizer.speech2text()
                                correct_affect_input = PatternRecognizerText2Speech.recognize_yes_or_no(
                                    correct_affect_input)

                                if correct_affect_input == 'Y':
                                    # print('\nnice!')
                                    playsound('modules/text2speech/generated_utterances/google_tts/nic.mp3')
                                    break
                                elif correct_affect_input == 'n':
                                    # print("\nlet's try once again!")
                                    playsound('modules/text2speech/generated_utterances/google_tts/lets_try_once.mp3')
                                elif correct_affect_input != 'Y' and correct_affect_input != 'n':
                                    print('\nplease, type in Y or n')

                        elif affect_presence_yes_or_no == 'n':
                            affect = 'no_affect'
                            # print("\nroger that! it will be marked as 'no_affect'")
                            playsound(
                                'modules/text2speech/generated_utterances/google_tts/roger_that_it_will_be_marked.mp3')
                            break
                        elif affect_presence_yes_or_no != 'Y' and affect_presence_yes_or_no != 'n':
                            print('\nplease, type in Y or n')

                    # create a db if it doesn't exist already
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

                elif response == MenuChoice.KEYBOARD_INPUT.value:
                    print('please, type in your record')
                elif response == MenuChoice.IMPORT_FROM_WAV.value:
                    print('provide the names of the .wav files')
                elif response == MenuChoice.PRINT_N_LAST_RECORDS.value:
                    print_n_last_records()
                elif response == MenuChoice.PERFORM_HYPOTHESIS_TEST.value:
                    perform_demo_hypothesis_test()
                elif response == MenuChoice.EXIT.value:
                    print('it was a pleasure! See you!')
                    break


if __name__ == '__main__':
    run_app()

# TODO: commit all changes to a new branch
