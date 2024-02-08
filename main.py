from enum import Enum
from typing import Union

from user_interface_base import UserInterface
from cli_user_interface import CLIUserInterface
from audio_user_interface import AudioUserInterface

INTERFACE_OPTIONS_DICT = {
    1: 'the app responds you via text',
    2: 'the app responds you via speech'
}


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


def choose_interface_type(interface_options: dict = None) -> Union[AppResponseInterface, None]:
    """

    Returns
    -------

    """

    print('choose the interface by typing in the number 1 or 2 \n'
          'note:\n'
          '1: the app responds you via text\n'
          '2: the app responds you via speech\n')
    interface_options = interface_options or INTERFACE_OPTIONS_DICT
    while True:
        try:
            interface_type = int(input())

        except ValueError:
            print(f'invalid input! it must be an integer corresponding to a valid interface option.\n'
                  'please, type in your choice once again\n')
        else:
            if interface_type in interface_options.keys():
                return AppResponseInterface(interface_type)
            else:
                print('the integer you typed in does not correspond to any valid interface option.\n'
                      'please, type in your choice once again\n')

                # return
                # with return: the menu is printed once again if the input was wrong
                # without return: the menu is printed only once since we loop inside this function


def get_user_interface(interface_type: AppResponseInterface) -> UserInterface:
    user_interface = None

    match interface_type:
        case AppResponseInterface.TEXT:
            user_interface = CLIUserInterface()
        case AppResponseInterface.SPEECH:
            user_interface = AudioUserInterface()

    return user_interface


def run_app():
    exit_the_app = False

    while True:  # choosing type of interface: text based or speech based

        interface_type = choose_interface_type()
        user_interface = get_user_interface(interface_type=interface_type)

        while True:

            user_interface.provide_menu_to_user()
            user_choice = user_interface.get_main_menu_response_from_user()

            match user_choice:
                case MenuChoice.VOICE_INPUT.value:

                    n_measurements = user_interface.get_number_of_measurements_from_user()
                    if n_measurements == 'quit_entering_the_number_of_measurements':
                        continue

                    all_user_voice_inputs = user_interface.iterative_input_of_measurements_from_user(
                        number_of_measurements=n_measurements)
                    average_systolic, average_diastolic, average_heart_rate = user_interface.calculate_average_rates(
                        all_measurements_raw_utterances=all_user_voice_inputs)

                    affect = user_interface.get_affect_from_user()

                    user_interface.add_measurements_to_db(systolic=average_systolic, diastolic=average_diastolic,
                                                          heart_rate=average_heart_rate, affect=affect)

                case MenuChoice.KEYBOARD_INPUT.value:
                    user_interface.keyboard_input()
                case MenuChoice.IMPORT_FROM_WAV.value:
                    user_interface.import_from_wav()
                case MenuChoice.PRINT_N_LAST_RECORDS.value:
                    user_interface.print_n_last_records()
                case MenuChoice.PERFORM_HYPOTHESIS_TEST.value:
                    user_interface.perform_demo_hypothesis_test()
                case MenuChoice.EXIT.value:
                    exit_the_app = True
                    print('exiting the app...\nit was a pleasure! See you!')
                    break

        if exit_the_app is True:
            break


if __name__ == '__main__':
    run_app()

# TODO: commit all changes to a new branch
