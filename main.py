import numpy as np
from modules.speech2text.speech_input import SpeechRecognizer
from modules.speech2text.pattern_recognizer import PatternRecognizerSpeech2Text
from modules.text2speech.pattern_recognizer import PatternRecognizerText2Speech
from databases.bp_hr_aff_database import BpHrAffectDatabase
from modules.hypothesis_testing.t_test import TTest
from enum import Enum
from playsound import playsound
from pathlib import Path

# TODO: store list of stuff which affects measurements

# TODO: on every line of code I should ask myself, whether this line realtes to input/output interaction with the user
#  if the following logic relates to the processing of the input!! then it should be function!!!!!!!!!!!!!1111!!

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


class MenuChoice(Enum):
    # TODO: вместо передачи строки "mse".
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


def run_app():
    while True:  # choosing type of interface: text based or speech based
        interface_type = int(input('choose the interface by typing in the number 1 or 2 \n'
                               'note:\n'
                               '1: the app responds you via text\n'
                               '2: the app responds you via speech\n'))

        if interface_type == AppResponseInterface.TEXT.value:

            while True:
                print_menu()
                # TODO: check whether the input is integer
                response = int(input())
                all_measurements = []

                # speech2text input
                # TODO: chnage to enum!!!!!
                if response == MenuChoice.VOICE_INPUT.value:  # TODO: use match/case instead of if/else

                    speech_recognizer = SpeechRecognizer()  # TODO: вынести либо до while, но лучше в модуль

                    print('please, type in the number of measurements you wanna take:')
                    # TODO: prevent typing in of characters, str etc. as well. NATURAL NUMBERS ONLY!
                    n_measurements = int(input())
                    if n_measurements <= 0:
                        print('the number of measurements must be a natural number. Restart the app. Otherwise, good bye!')
                        break
                    print(f'\nok! we are ready to record {n_measurements} measurements')
                    print(f'\nplease prepare your blood pressure monitor and give your input in the following format:')
                    print("\n'systolic #number#, diastolic #number#, heart rate #number#'")

                    # TODO: input/output interation remains inside the main.py module
                    #  but the processing of the inputs must be performed outside the main.py
                    for measurement in range(n_measurements):
                        # kukaracha
                        while True:
                            # TODO: suggestion to take a break between measurements

                            #  measurement + 1 so that we show user his measurements starting from 1, not from 0
                            ready_for_measurement = input(
                                f'\nhave you done your {measurement + 1} measurement? are you ready to input it? [Y/n] ')
                            if ready_for_measurement == 'Y':  # TODO: Добавить yes, y etc. через Enum
                                print('we are listening to you...')
                                # FIXME: speech_recognition.exceptions.UnknownValueError if there is no speech input

                                # TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”)
                                # TODO: try to input in other languages
                                user_voice_input = speech_recognizer.speech2text()
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
                                        user_voice_input = speech_recognizer.speech2text()
                                        print(f'measurement #{measurement + 1}: {user_voice_input}')
                                    else:  # correctly_recognized != 'Y' and correctly_recognized != 'n':
                                        print('\nplease, type in Y or n')

                                # if a measurement was successfully recognized we quit the first 'while' loop
                                # and go to the next iteration/measurement inside 'for' loop
                                break
                            elif ready_for_measurement == 'n':
                                print('\nnot a problem! we are waiting for you :)')
                            elif ready_for_measurement != 'Y' and ready_for_measurement != 'n':
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
                    print(f'\nhere are the average rates from {n_measurements} measurement(-s): \nsys: {systolic}'
                          f'\ndia: {diastolic} \nhr: {heart_rate}')

                    # add a affect
                    while True:
                        affect_presence = input(
                            '\ndo you do any activities (gym, work etc.), '
                            'take any medication or consume any substances (e.g. antihypertensives, coffee etc.)\n'
                            'the effects of which you want to control regarding your blood pressure? [Y/n] ')

                        if affect_presence == 'Y':

                            affect = input('\nwhat can potentially affect your rates? please, tell me what it is\n')
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

                        elif affect_presence == 'n':
                            affect = 'no_affect'
                            print("\nroger that! it will be marked as 'no_affect'")
                            break
                        elif affect_presence != 'Y' and affect_presence != 'n':
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
                    print('here are your last records:')
                elif response == MenuChoice.PERFORM_HYPOTHESIS_TEST.value:
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
                    sys_rows_affected = demo_bp_hr_aff_db.retrieve_measurements_for_demo_test(connection=demo_connection,
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

                elif response == MenuChoice.EXIT.value:
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
                    playsound('modules/text2speech/generated_utterances/google_tts/please_tell_me_the_number_of_measureme.mp3')
                    number_of_measurements_user_voice_input = speech_recognizer.speech2text()
                    print(number_of_measurements_user_voice_input)
                    n_measurements = PatternRecognizerText2Speech.recognize_number(number_of_measurements_user_voice_input)

                    if n_measurements <= 0: # TODO: other exceptions as well!
                        # the number of measurements must be a natural number. Restart the app. Otherwise, good bye!
                        playsound('modules/text2speech/generated_utterances/google_tts/the_number_of_measurements_must_be_a_natural_number_Restart.mp3')
                        break
                    # TODO: match-case: 1, 2, 3, 4 measurements
                    # print(f'\nok! we are ready to record {n_measurements} measurements')
                    playsound('modules/text2speech/generated_utterances/google_tts/ok_we_are_ready_to_take_m.mp3')
                    # print(f'\nplease prepare your blood pressure monitor and give your input in the following format:')
                    playsound('modules/text2speech/generated_utterances/google_tts/please_prepare_your_blood_pressure_monitor_and_give_your.mp3')
                    # print("\n'systolic #number#, diastolic #number#, heart rate #number#'")
                    playsound('modules/text2speech/generated_utterances/google_tts/pronounce_systolic_and_then_provide_a_number_say_diastolic_and_then_a_number_eventually_pronounce_h.mp3')

                    # TODO: input/output interation remains inside the main.py module
                    #  but the processing of the inputs must be performed outside the main.py
                    for measurement in range(n_measurements):
                        # kukaracha
                        while True:
                            # TODO: suggestion to take a break between measurements

                            #  measurement + 1 so that we show user his measurements starting from 1, not from 0
                            ready_for_measurement = input(
                                f'\nhave you done your {measurement + 1} measurement? are you ready to input it? [Y/n] ')
                            if ready_for_measurement == 'Y':  # TODO: Добавить yes, y etc. через Enum
                                print('we are listening to you...')
                                # FIXME: speech_recognition.exceptions.UnknownValueError if there is no speech input

                                # TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”)
                                # TODO: try to input in other languages
                                user_voice_input = speech_recognizer.speech2text()
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
                                        user_voice_input = speech_recognizer.speech2text()
                                        print(f'measurement #{measurement + 1}: {user_voice_input}')
                                    else:  # correctly_recognized != 'Y' and correctly_recognized != 'n':
                                        print('\nplease, type in Y or n')

                                # if a measurement was successfully recognized we quit the first 'while' loop
                                # and go to the next iteration/measurement inside 'for' loop
                                break
                            elif ready_for_measurement == 'n':
                                print('\nnot a problem! we are waiting for you :)')
                            elif ready_for_measurement != 'Y' and ready_for_measurement != 'n':
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
                    print(f'\nhere are the average rates from {n_measurements} measurement(-s): \nsys: {systolic}'
                          f'\ndia: {diastolic} \nhr: {heart_rate}')

                    # add a affect
                    while True:
                        affect_presence = input(
                            '\ndo you do any activities (gym, work etc.), '
                            'take any medication or consume any substances (e.g. antihypertensives, coffee etc.)\n'
                            'the effects of which you want to control regarding your blood pressure? [Y/n] ')

                        if affect_presence == 'Y':

                            affect = input('\nwhich affect do you take then? please, typy in: ')
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

                        elif affect_presence == 'n':
                            affect = 'no_affect'
                            print("\nroger that! it will be marked as 'no_affect'")
                            break
                        elif affect_presence != 'Y' and affect_presence != 'n':
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
                    print('here are your last records:')
                elif response == MenuChoice.PERFORM_HYPOTHESIS_TEST.value:
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
                    sys_rows_affected = demo_bp_hr_aff_db.retrieve_measurements_for_demo_test(connection=demo_connection,
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

                elif response == MenuChoice.EXIT.value:
                    print('it was a pleasure! See you!')
                    break


if __name__ == '__main__':
    run_app()

# TODO: commit all changes to a new branch
