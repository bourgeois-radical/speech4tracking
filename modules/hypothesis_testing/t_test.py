"""

We need a paired t-test (NOT independent two-sample t-test, SINCE we don't wanna check
whether two groups differ from each other), because measurements are paired and the person is the same

Null Hypothesis: the means of (sys/dia/hr) are the same in the 2 groups (affected and not)
If the null is rejected: means are different

two tailed - why?

https://www.jmp.com/en_ch/statistics-knowledge-portal/t-test.html

https://thedatascientist.com/how-to-do-a-t-test-in-python/

https://ec.europa.eu/eurostat/web/products-eurostat-news/-/edn-20210929-1

"""

# TODO: check, whether the distributions approximately normal

from scipy.stats import ttest_rel
from typing import List
import modules.hypothesis_testing.parameters
import numpy as np


class TTest:
    def __init__(self, provided_p_value = None):
        if provided_p_value is None:
            self.specified_p_value = modules.hypothesis_testing.parameters.PREDEFINED_P_VALUE
        else:
            self.specified_p_value = provided_p_value

    def sys_paired_t_test(self, not_affected: List = None, affected: List = None, affected_by: str = None):

        t_stat, p_value = ttest_rel(not_affected, affected)

        # TODO: how to understand, in which direction it is affected? Does the intake lower or raise the pressure?
        #  maybe one-sided that's why?
        # TODO: Read on t_stat
        # TODO: t_stat minus sign tells us about the direction
        #  (grater [coffee] - less = +) or (less - grater [coffee] = -)

        print(f'results: \nt_stat: {np.round(t_stat, 3)}, p_value: {np.round(p_value, 3)}')

        if p_value <= self.specified_p_value and t_stat < 0:
            print('\ninterpretation:')
            print(f'{affected_by} intake raises your systolic blood pressure! be careful with it and consult your doctor.')

        return t_stat, p_value

    def dia_paired_t_test(self, affected_by: str):
        pass

    def hr_paired_t_test(self, affected_by: str):
        pass




