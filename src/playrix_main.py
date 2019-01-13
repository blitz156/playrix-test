import datetime
import pandas as pd


COHORT_ANALYSIS_FILTERS = {
    'mobile_app': 2,
    'date__gt': datetime.datetime(2016, 5, 2),
    'date__lt': datetime.datetime(2016, 5, 10),
}


# Функция, которая подсчитывает RPI на промежуток заданный промежуток,
# При этом начальная дата - дата из наших фильров
# Конечная дата - начальная дата + промежуток delta
def _get_rpi_by_date_range(installs_aggregations, purchases, delta):
    # Фильтруем покупки:
    # 1. Дата устанвки игры более заданной в фильтрах значением date__gt
    # 2. Дата устанвки игры менее заданной в фильтрах значением date__lt
    # 3. Дата покупки более заданной в фильтрах значением date__gt
    # 4. Дата покупки менее заданной в фильтрах значением date__gt + delta
    # Группируем по стране и считаем сумму покупок
    result = \
        purchases[purchases['install_date'] >= COHORT_ANALYSIS_FILTERS['date__gt']] \
        [purchases['install_date'] < COHORT_ANALYSIS_FILTERS['date__lt']] \
        [purchases['created'] >= COHORT_ANALYSIS_FILTERS['date__gt']] \
        [purchases['created'] < COHORT_ANALYSIS_FILTERS['date__gt'] + datetime.timedelta(delta)] \
            .groupby(['country'], as_index=False) \
            .agg({'revenue': 'sum'}) \
            .rename(columns={'revenue': 'RPI{}'.format(delta)})

    # Вычисляем RPI, где RPI = сумма покупок за период / количество всех установок для конкретной старны
    # P.S. Вообще согласно задания RPI должен считаться иначе, но не вижу никакой привязки покупок к конкретным пользователям
    for index, row in result.iterrows():
        result.set_value(
            index,
            'RPI{}'.format(delta),
            row['RPI{}'.format(delta)] / installs_aggregations[installs_aggregations['country'] == row['country']].iloc[0]['installs']
        )

    return result


def create_cohort_analysis(installs_file, purchases_file):
    installs = pd.read_csv(installs_file, parse_dates=['created'])
    purchases = pd.read_csv(purchases_file, parse_dates=['created', 'install_date'])

    purchases = purchases[purchases['mobile_app'] == 2]
    installs = installs[installs['mobile_app'] == 2]

    # Подсчитываем количество установок в каждой стране
    installs_aggregations = \
        installs[installs['created'] >= COHORT_ANALYSIS_FILTERS['date__gt']][installs['created'] < COHORT_ANALYSIS_FILTERS['date__lt']] \
            .groupby(['mobile_app', 'country'], as_index=False) \
            .count() \
            .rename(columns={'created': 'installs'})[['country', 'installs']]

    # Посчитываем RPI{X}
    rpi_array = [_get_rpi_by_date_range(installs_aggregations, purchases, i) for i in range(1, 11)]

    # Мержим результаты
    result = installs_aggregations
    for rpi in rpi_array:
        result = pd.merge(result, rpi, on=['country', 'country'], how='outer')

    # Сортируем по установкам и оставляем только нужные столбцы в правильном порядке
    result = result.sort_values(by=['installs'], ascending=False)[['country', 'installs', 'RPI1', 'RPI2', 'RPI3', 'RPI4', 'RPI5', 'RPI6', 'RPI7', 'RPI8', 'RPI9', 'RPI10']]
    return result


