import argparse
import random
import json

import pendulum

from cal import workcal


def pick_a_time(data):
    all_data = []
    for v, w in data.items():
        temp = []
        for i in range(w):
            temp.append(v)
        all_data.extend(temp)

    n = random.randint(0, len(all_data) - 1)
    return int(all_data[n])


def gen_dataframe(df, user, task, start_at, end_at):
    total_hours = 0
    total_minutes = 0
    for index_label, row_series in df.iterrows():
        s = f"{pick_a_time(start_at):02d}:{random.randrange(0, 60):02}"
        e = f"{pick_a_time(end_at):02d}:{random.randrange(0, 60):02}"
        timestamp_notes = "{0}-{1}".format(s, e)
        duration = pendulum.parse(e) - pendulum.parse(s)
        total_hours += duration.hours
        total_minutes += duration.minutes
        time = "{0}h {1}m".format(str(duration.hours), str(duration.minutes))

        df.at[index_label, 'User'] = user
        df.at[index_label, 'Task'] = task
        df.at[index_label, 'Time'] = time
        df.at[index_label, 'Timestamp Notes'] = timestamp_notes
    df = df.append(
        {
            'Time':
            '{0}h {1}m'.format(total_hours + int(total_minutes / 60),
                               total_minutes % 60)
        },
        ignore_index=True)
    return df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process timecamp.')
    parser.add_argument('year',
                        metavar='y',
                        type=int,
                        help='an integer for the year ex:2020')
    parser.add_argument('month',
                        metavar='m',
                        type=int,
                        help='an integer for the year ex:1...12')
    parser.add_argument('ignore_date',
                        metavar='ignore',
                        type=int,
                        nargs="+",
                        help='an integer list for the date ex:1...12')
    args = parser.parse_args()

    df = workcal(args.year, args.month, args.ignore_date)

    with open('ppl.json', 'r') as reader:
        jf = json.loads(reader.read())

    for data in jf:
        df = gen_dataframe(df.copy(), data["name"], data["task"],
                           data["start_at"], data["end_at"])

        df.to_excel("{0}.xlsx".format(data["name"].replace(" ", "")),
                    index=False,
                    header=True)
