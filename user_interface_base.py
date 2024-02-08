from typing import Sequence, Optional
import abc

import numpy as np

from databases.bp_hr_aff_database import BpHrAffectDatabase
from modules.hypothesis_testing.t_test import TTest
from modules.speech2text.pattern_recognizer import PatternRecognizerSpeech2Text
from modules.speech2text.speech_input import SpeechRecognizer


class UserInterface(abc.ABC):

    def __init__(self):
        self.demo_bp_hr_aff_db = BpHrAffectDatabase()
        self.pattern_recognizer = PatternRecognizerSpeech2Text()
        self.speech_recognizer_instance = SpeechRecognizer()
        self.MENU_OPTIONS_DICT = {
            1: 'add a record (speech2text)',
            2: 'add a record (keyboard)',
            3: 'add a record(-s) (.wav file)',
            4: 'print n last records',
            5: 'perform a hypothesis test',
            6: 'exit'
        }
        self.ALLOWED_NUMBER_OF_MEASUREMENTS_LIST = [1, 2, 3]

    @abc.abstractmethod
    def provide_menu_to_user(self) -> None:
        pass

    def get_main_menu_response_from_user(self, menu_options: dict = None) -> int | None:
        menu_options = menu_options or self.MENU_OPTIONS_DICT
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

    @abc.abstractmethod
    def get_number_of_measurements_from_user(self, allowed_number_of_measurements: Optional[Sequence[int]] = None) \
            -> int | str:
        pass

    @abc.abstractmethod
    def iterative_input_of_measurements_from_user(self, number_of_measurements: int) -> Sequence[str]:
        pass

    @abc.abstractmethod
    def get_affect_from_user(self) -> str:
        pass

    def perform_demo_hypothesis_test(self):
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

        demo_connection = self.demo_bp_hr_aff_db.create_demo_connection(db_path='./databases/demo.db')
        # demo_bp_hr_aff_db.initialize_fake_measurements(demo_connection)

        # retrieve two paired samples for diastolic
        sys_rows_affected = self.demo_bp_hr_aff_db.retrieve_measurements_for_demo_test(
            connection=demo_connection,
            rate_of_interest='sys',
            affected_by='coffee')

        sys_rows_not_affected = self.demo_bp_hr_aff_db.retrieve_measurements_for_demo_test(
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

    def calculate_average_rates(self, all_measurements: Sequence[str]) -> Sequence[int]:
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
        all_measurements = (
            self.pattern_recognizer.blood_pressure_heart_rate_from_voice(recognized_voice_inputs=all_measurements))
        # count the mean from n (the number is provided by user) measurements
        print(f'printing all_measurements_raw_utterances: {all_measurements}')
        all_measurements_np = np.mean(np.array(all_measurements), axis=1)
        systolic = all_measurements_np[0]
        diastolic = all_measurements_np[1]
        heart_rate = all_measurements_np[2]

        return systolic, diastolic, heart_rate


    def keyboard_input(self):
        raise NotImplementedError('Sorry, keyboard input is not available at the moment. We are working on '
                                  'implementing this feature and appreciate your understanding.')

    def import_from_wav(self):
        raise NotImplementedError('Sorry, import from wav-files is not available at the moment. '
                                  'We are working on implementing this feature and appreciate your understanding.')

    def print_n_last_records(self):
        raise NotImplementedError('Sorry, last-records-printing is not available at the moment. '
                                  'We are working on implementing this feature and appreciate your understanding.')

    @abc.abstractmethod
    def db_error_message_to_user(self):
        pass

    @abc.abstractmethod
    def db_success_message_to_user(self):
        pass

    def add_measurements_to_db(self, systolic, diastolic, heart_rate, affect):
        bp_hr_aff_db = BpHrAffectDatabase()
        connection = bp_hr_aff_db.create_connection(db_path='./databases/test.db')

        if connection is not None:
            bp_hr_aff_db.create_table(connection=connection)
        else:
            self.db_error_message_to_user()

        # add measurements to the db
        bp_hr_aff_db.insert_row(connection=connection, systolic=systolic, diastolic=diastolic, heart_rate=heart_rate,
                                affect=affect)

        # close connection to the db
        bp_hr_aff_db.close_connection(connection=connection)

        self.db_success_message_to_user()

        return  # actually, returns None. It's a procedure in normal programming languages
