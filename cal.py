import pandas as pd
import pendulum
from workalendar.asia import Taiwan


def cal_festival(year_list):
    cal = Taiwan()
    date_list = []
    for year in year_list:
        for x, v in cal.holidays(year):
            date_list.append([str(x), v])
    df = pd.DataFrame(data=date_list, columns=['date', 'festival'])
    return df


def date_to_week(start_time, end_time):
    df = pd.DataFrame()
    df['date'] = pd.date_range(start=start_time, end=end_time)
    df['day_of_week'] = df['date'].dt.dayofweek + 1
    df['date'] = df['date'].map(lambda x: x.strftime('%Y-%m-%d'))
    return df


def workcal(year, month, ignore):
    dt_taipei = pendulum.datetime(year, month, 1, tz='Asia/Taipei')
    start_date = dt_taipei.start_of('month').to_date_string()
    end_date = dt_taipei.end_of('month').to_date_string()
    df_festival = cal_festival([year])
    date_festival_list = df_festival["date"].tolist()
    date_festival_list += [
        pendulum.datetime(year, month, d, tz='Asia/Taipei').to_date_string()
        for d in ignore
    ]
    df_date = date_to_week(start_date, end_date)
    df_filter_date = df_date[~df_date["date"].isin(date_festival_list)].copy()
    df = df_filter_date[df_filter_date["day_of_week"] <= 5].drop(
        columns=['day_of_week'])
    return df
