import pandas as pd
from pandas.testing import assert_frame_equal

from playrix_main import create_cohort_analysis

result = create_cohort_analysis('csv_for_test/installs.csv', 'csv_for_test/purchases.csv')
test_right_result = pd.read_csv('csv_for_test/result.csv')

assert_frame_equal(result.reset_index(drop=True), test_right_result.reset_index(drop=True), check_dtype=False)
print('---------- TEST OK ----------')
