import datetime
import pandas as pd


COHORT_ANALYSIS_FILTERS = {
    'mobile_app': 2,
    'date__gt': datetime.datetime(2016, 5, 2),
    'date__lt': datetime.datetime(2016, 5, 10),
}


# Функция, которая подсчитывает RPI на промежуток заданный delta,
# При этом начальная дата - дата из наших фильров
# Конечная дата - начальная дата + промежуток delta
def _get_rpi_by_date_range(installs_aggregations, purchases, delta, filters):
    # Фильтруем покупки в цикле:
    # 1. День установки поочередно каждый в промежутке фильтрации
    # 2. Дата покупки начиная с фильтруемого дня в п.1
    # 3. Дата покупки менее даты п.1 + delta days
    filtered_purchases = [
        purchases
            [purchases['install_date'] >= filters['date__gt'] + datetime.timedelta(index)] \
            [purchases['install_date'] < filters['date__gt'] + datetime.timedelta(index + 1)] \
            [purchases['created'] >= filters['date__gt'] + datetime.timedelta(index)]  \
            [purchases['created'] < filters['date__gt'] + datetime.timedelta(delta + index)]
        for index in range(0, (filters['date__lt'] - filters['date__gt']).days)
    ]
    filtered_purchases = pd.concat(filtered_purchases)

    # Группируем по стране и считаем сумму покупок
    result = filtered_purchases.groupby(['country'], as_index=False) \
        .agg({'revenue': 'sum'}) \
        .rename(columns={'revenue': 'RPI{}'.format(delta)})

    # Вычисляем RPI, где RPI = сумма покупок за период / количество всех установок для конкретной старны
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

    purchases = purchases[purchases['mobile_app'] == COHORT_ANALYSIS_FILTERS['mobile_app']]
    installs = installs[installs['mobile_app'] == COHORT_ANALYSIS_FILTERS['mobile_app']]

    # Подсчитываем количество установок в каждой стране
    installs_aggregations = \
        installs[installs['created'] >= COHORT_ANALYSIS_FILTERS['date__gt']][installs['created'] < COHORT_ANALYSIS_FILTERS['date__lt']] \
            .groupby(['mobile_app', 'country'], as_index=False) \
            .count() \
            .rename(columns={'created': 'installs'})[['country', 'installs']]

    # Посчитываем RPI{X}
    rpi_array = [_get_rpi_by_date_range(installs_aggregations, purchases, i, COHORT_ANALYSIS_FILTERS) for i in range(1, 11)]

    # Мержим результаты
    result = installs_aggregations
    for rpi in rpi_array:
        result = pd.merge(result, rpi, on=['country', 'country'], how='outer')

    # Сортируем по установкам и оставляем только нужные столбцы в правильном порядке
    result = result.sort_values(by=['installs'], ascending=False)[['country', 'installs', 'RPI1', 'RPI2', 'RPI3', 'RPI4', 'RPI5', 'RPI6', 'RPI7', 'RPI8', 'RPI9', 'RPI10']]
    return result


