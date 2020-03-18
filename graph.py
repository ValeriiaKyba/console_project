import math
import datetime
import pylab

from db import get_stats_by_field, get_count_by_cloudiness, get_freq


def draw_graph(fields, period):
    list_of_xlist = []
    list_of_ylist = []
    for field in fields:
        res = get_stats_by_field(field, period)
        xlist = [i[3] for i in sorted(res, key=lambda x: datetime.datetime.strptime(x[3], '%Y-%m-%d'))]
        ylist = [(i[0], i[1], i[2]) for i in sorted(res, key=lambda x: x[3])]
        list_of_xlist.append(xlist)
        list_of_ylist.append(ylist)
    for xl, yl in zip(list_of_xlist, list_of_ylist):
        pylab.plot(xl, yl)
        pylab.xticks(rotation=90)
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
    pylab.figlegend()
    pylab.show()


def draw_hist(field_id, date):
    freq = get_freq(field_id, date)
    values = [(i[0], [i[0] for j in range(i[1])]) for i in freq]
    for i in values:
        pylab.hist(i[1], label=str(i[0]))

    pylab.figlegend()

    pylab.show()
