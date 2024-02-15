from typing import Sequence

from user_interface_base import UserInterface


class CLUserInterface(UserInterface):

    def __init__(self):
        super().__init__()

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

        return

    def get_number_of_measurements_from_user(self, allowed_number_of_measurements: Sequence[int] = None) -> int | str:
        allowed_number_of_measurements = allowed_number_of_measurements or self.ALLOWED_NUMBER_OF_MEASUREMENTS_LIST
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

    def iterative_input_of_measurements_from_user(self, number_of_measurements: int) -> Sequence[str]:
        """

        Parameters
        ----------
        number_of_measurements : int
            Number of measurements a user wants to make

        Returns
        -------
         all_measurements_raw_utterances : Sequence[str]
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
                    user_voice_input = self.speech_recognizer_instance.speech2text()
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
                            user_voice_input = self.speech_recognizer_instance.speech2text()
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

    def get_affect_from_user(self) -> str:
        """This function helps to input an affect. Affect is something what can potentially influence blood
        pressure rates.

        Returns
        -------

        affect : str
            Substance, activity etc.

        """

        while True:
            is_there_an_affect = input(
                '\ndo you do any activities (gym, work etc.), '
                'take any medication or consume any substances (e.g. antihypertensives, coffee etc.)\n'
                'the effects of which you want to control regarding your blood pressure? [Y/n] ')

            if is_there_an_affect == 'Y':

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

            elif is_there_an_affect == 'n':
                affect = 'no_affect'
                print("\nroger that! it will be marked as 'no_affect'")
                break
            else:
                print('\nplease, type in Y or n')

        return affect

    def db_error_message_to_user(self):
        print('error! cannot create the databases connection')

    def db_success_message_to_user(self):
        print('the measurement has been successfully added to database!')

    def calculate_average_rates(self, all_measurements_raw_utterances: Sequence[str]) -> Sequence[int]:

        systolic, diastolic, heart_rate = super().calculate_average_rates(all_measurements_raw_utterances)
        print(f'\nhere are the average rates from {len(all_measurements_raw_utterances)} measurement(-s): \nsys: {systolic}'
              f'\ndia: {diastolic} \nhr: {heart_rate}')

        return systolic, diastolic, heart_rate
