import os
from typing import Sequence


from playsound import playsound

from modules.text2speech.pattern_recognizer import PatternRecognizerText2Speech
from modules.text2speech.tts_current_measurement import save_current_voice_input_as_mp3
from user_interface_base import UserInterface


class AudioUserInterface(UserInterface):

    def provide_menu_to_user(self) -> None:
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

        playsound(
            'modules/text2speech/generated_utterances/google_tts/'
            'what_are_we_gonna_do_1_add_a_record_2_add_a_record_via_keyboard_3_add_records_from_wav_files_4_print_last_re.mp3'
        )

        return

    def get_number_of_measurements_from_user(self, allowed_number_of_measurements: Sequence[int] = None) -> int | str:
        allowed_number_of_measurements = allowed_number_of_measurements or self.ALLOWED_NUMBER_OF_MEASUREMENTS_LIST

        # print('please, type in the number of measurements the user wanna take
        playsound('modules/text2speech/generated_utterances/google_tts/please_tell_me_the_number_of_measureme.mp3')

        while True:
            number_of_measurements_user_voice_input = self.speech_recognizer_instance.speech2text()
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

        playsound('modules/text2speech/generated_utterances/google_tts/please_prepare_your_blood_pressure_monitor_and_give_your.mp3')
        playsound('modules/text2speech/generated_utterances/google_tts/pronounce_systolic_and_then_provide_a_number.mp3')

        return n_measurements

    def iterative_input_of_measurements_from_user(self, number_of_measurements: int) -> Sequence[str]:
        """

            Parameters
            ----------
            number_of_measurements

            Returns
            -------

            """

        def block_of_generated_utterances_prepare_blood_pressure_monitor_and_pronounce_measurements():
            playsound('modules/text2speech/generated_utterances/google_tts/please_prepare_your_blood_pressure_monitor_and_give_your.mp3')
            playsound('modules/text2speech/generated_utterances/google_tts/pronounce_systolic_and_then_provide_a_number.mp3')

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
                    is_ready_to_input = self.speech_recognizer_instance.speech2text()
                    is_ready_to_input = PatternRecognizerText2Speech.recognize_yes_or_no(
                        is_ready_to_input)

                    if is_ready_to_input is True:  # TODO: Add yes, y etc. with Enum???
                        playsound('modules/text2speech/generated_utterances/google_tts/we_are_listening.mp3')
                        # FIXME: speech_recognition.exceptions.UnknownValueError if there is no speech input
                        # TODO: 132/88 mmHg !!!!!!!(often spoken “132 over 88”)
                        # TODO: try to input in other languages (it seems, it doesn't work)

                        # TODO: pattern! define a function for generation of current measurements
                        user_voice_input = self.speech_recognizer_instance.speech2text()
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
                            is_correctly_recognized = self.speech_recognizer_instance.speech2text()
                            is_correctly_recognized = PatternRecognizerText2Speech.recognize_yes_or_no(
                                is_correctly_recognized)
                            if is_correctly_recognized is True:  # TODO: change to MATCH-CASE + use ENUM
                                all_measurements.append(user_voice_input)
                                break
                            elif is_correctly_recognized is False:
                                # TODO: manual correction
                                playsound(
                                    'modules/text2speech/generated_utterances/google_tts/lets_try_once.mp3')
                                break  # nested loop

                            else:
                                playsound(
                                    'modules/text2speech/generated_utterances/google_tts/I_didnt_get_you_please_just_s.mp3')
                    # else:
                    # TODO: user is not ready to input
                    break  # main while loop and go to the for loop

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

    def get_affect_from_user(self) -> str:
        """

            Parameters
            ----------
            speech_recognizer_instance

            Returns
            -------

            """
        while True:

            playsound(
                'modules/text2speech/generated_utterances/google_tts/do_you_do_any_activities_gym_work_etc_take_any_medication.mp3')
            is_there_an_affect = self.speech_recognizer_instance.speech2text()
            is_there_an_affect = PatternRecognizerText2Speech.recognize_yes_or_no(is_there_an_affect)

            if is_there_an_affect is True:

                playsound(
                    'modules/text2speech/generated_utterances/google_tts/what_can_potentially_affect_your_rates_pleas.mp3')
                affect =  self.speech_recognizer_instance.speech2text()
                affect = affect.strip()

                save_current_voice_input_as_mp3(affect)

                if len(affect) > 0:

                    playsound(
                        'modules/text2speech/generated_utterances/google_tts/is_your_input_correct.mp3')
                    playsound('modules/text2speech/generated_utterances/current_measurement.mp3')
                    #  immediately delete file after having just created it
                    if os.path.exists('modules/text2speech/generated_utterances/current_measurement.mp3'):
                        os.remove('modules/text2speech/generated_utterances/current_measurement.mp3')
                    else:
                        print('The file does not exist')

                    is_affect_input_correct = self.speech_recognizer_instance.speech2text()
                    is_affect_input_correct = PatternRecognizerText2Speech.recognize_yes_or_no(
                        is_affect_input_correct)

                    if is_affect_input_correct is True:
                        playsound('modules/text2speech/generated_utterances/google_tts/nic.mp3')
                        break
                    elif is_affect_input_correct is False:
                        playsound('modules/text2speech/generated_utterances/google_tts/lets_try_once.mp3')
                        continue
                    else:
                        playsound(
                            'modules/text2speech/generated_utterances/google_tts/I_didnt_get_you_please_just_s.mp3')
                        continue

            elif is_there_an_affect is False:
                affect = 'no_affect'
                playsound(
                    'modules/text2speech/generated_utterances/google_tts/roger_that_it_will_be_marked.mp3')
                break
            else:
                print('\nplease, type in Y or n')

        return affect

    def db_error_message_to_user(self):
        playsound('modules/text2speech/generated_utterances/google_tts/error_cannot_create_the_databa.mp3')

    def db_success_message_to_user(self):
        playsound('modules/text2speech/generated_utterances/google_tts/the_measurement_has_been_successfully.mp3')

    def calculate_average_rates_speech_based(self, all_measurements: Sequence[str]) -> Sequence[int]:
        """After having collected all measurements (str) in one list, we must find the rates (int) of interest.

        Parameters
        ----------
        all_measurements : Sequence[str]

        Returns
        -------
        systolic : int
        diastolic : int
        heart_rate : int

        """
        systolic, diastolic, heart_rate = super().calculate_average_rates(all_measurements=all_measurements)

        average_rates = ''
        # len(all_measurements[0]) because [[120, 121], [80, 90], [60, 70]]
        if len(all_measurements[0]) == 1:
            average_rates = (f'only one measurement has been taken. systolic: {systolic} diastolic: {diastolic} '
                             f'heart rate: {heart_rate}')
        elif len(all_measurements[0]) > 1:
            average_rates = (f'here are the average rates from {len(all_measurements)} measurements. '
                             f'systolic: {systolic} diastolic: {diastolic} heart rate: {heart_rate}')
        # TODO: add utterance: 'here are your average rates'
        save_current_voice_input_as_mp3(average_rates)
        # TODO: rename 'current_measurement' to 'current_input' or whatever.
        #  Use an f string with a variable so that one can refactor it
        playsound('modules/text2speech/generated_utterances/current_measurement.mp3')

        #  immediately delete file after having just created it
        if os.path.exists('modules/text2speech/generated_utterances/current_measurement.mp3'):
            os.remove('modules/text2speech/generated_utterances/current_measurement.mp3')
        else:
            print('The file does not exist')

        return systolic, diastolic, heart_rate
