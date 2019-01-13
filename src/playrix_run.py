import time

from playrix_main import create_cohort_analysis

t0 = time.time()
result = create_cohort_analysis('csv/installs.csv', 'csv/purchases.csv')

result.to_csv('output/result.csv', index=False)

print(result)
print('work time = {}с'.format(time.time() - t0))
