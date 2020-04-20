import datetime
import pylab

from db import get_stats_by_field, get_count_by_cloudiness, get_freq


def draw_graph(fields, period, years):

    for year in years:
        for field in fields:
            new_period = (f'{year}-{period[0]}', f'{year}-{period[1]}')
            res = get_stats_by_field(field, new_period)
            xlist, ylist = [], []
            sorted_res = sorted(res, key=lambda x: datetime.datetime.strptime(x[3], '%Y-%m-%d'))
            min_list = []
            avg_list = []
            max_list = []

            for i in sorted_res:
                date_ = datetime.datetime.strptime(i[3], '%Y-%m-%d')
                xlist.append(date_.month + date_.day/31)
                avg_list.append(i[0])
                min_list.append(i[1])
                max_list.append(i[2])

            pylab.plot(xlist, min_list, label=f'min for {field} {year}')
            pylab.plot(xlist, avg_list, label=f'avg for {field} {year}')
            pylab.plot(xlist, max_list, label=f'max for {field} {year}')
            pylab.ylabel("Average weighted")
            pylab.xlabel("Month")
            pylab.xticks(rotation=90)
    pylab.figlegend()
    pylab.show()


def draw_clean(field_id):
    counts = get_count_by_cloudiness(field_id)

    sorted_counts = sorted(counts, key=lambda x: x[0])
    xlist = [i[0] for i in sorted_counts]
    ylist1 = [i[1] for i in sorted_counts]
    ylist2 = [i[2] for i in sorted_counts]
    ylist3 = [i[3] for i in sorted_counts]

    pylab.plot(xlist, ylist1, color='b', label='Clear')
    pylab.plot(xlist, ylist2, color='g', label='Clouded')
    pylab.plot(xlist, ylist3, color='r', label='Mixed')
    pylab.title("Analysis of cloudiness of the field = " + field_id)
    pylab.ylabel("Count of days")
    pylab.xlabel("Month")
    pylab.figlegend()
    pylab.show()


def draw_hist(field_id, date):
    freq = get_freq(field_id, date)
    values = [(i[0], [i[0] for j in range(i[1])]) for i in freq]
    for i in values:
        pylab.hist(i[1], label=str(i[0]))
    pylab.title("Frequency histogram of the field = " + field_id + " on " + date)
    pylab.ylabel("Frequencies")
    pylab.xlabel("Unique values")
    pylab.show()
