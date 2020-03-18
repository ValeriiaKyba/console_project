from __future__ import print_function, unicode_literals
import datetime
from pprint import pprint

from PyInquirer import prompt, Separator

from examples import custom_style_2
from const import *
from db import get_fields_list
from graph import draw_graph, draw_clean, draw_hist


def validate_date_str(s):
    try:
        datetime.datetime.strptime(s, '%Y%-m%-%d')
    except Exception as e:
        print(e)
        return False
    return True


main_question = [
    {
        'type': 'list',
        'name': 'theme',
        'message': 'Що бажаєте зробити?',
        'choices': [
            display_graph,
            display_clean,
            display_hist,
            Separator(),
            exit_
        ]
    },
    {
        'type': 'list',
        'name': 'period',
        'message': 'За який період бажаєте відобразити?',
        'when': lambda ans: ans.get('theme') == display_graph,
        'choices': [
            all_period,
            choose_period,
            Separator(),
            exit_
        ]
    },
    {
        'type': 'input',
        'name': 'start_period',
        'message': 'Введіть початок періоду. (Рік-місяць-день)',
        'when': lambda ans: ans.get('period') == choose_period,
        'validate': validate_date_str
    },
    {
        'type': 'input',
        'name': 'end_period',
        'message': 'Введіть початок періоду.',
        'when': lambda ans: ans.get('start_period'),
        'validate': validate_date_str
    },
    {
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Оберіть поля які бажаєте бачити на графіку.',
        'name': 'fields',
        'choices': get_fields_list(),
        'when': lambda ans: ans.get('theme') == display_graph,
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    },
    {
        'type': 'list',
        'name': 'clean_vis',
        'message': 'Яке поле відобразити?',
        'when': lambda ans: ans.get('theme') == display_clean,
        'choices': get_fields_list()
    },
    {
        'type': 'list',
        'name': 'hist',
        'message': 'Яке поле відобразити?',
        'when': lambda ans: ans.get('theme') == display_hist,
        'choices': get_fields_list()
    },
    {
        'type': 'input',
        'name': 'date_hist',
        'message': 'Введіть дату. (Рік-місяць-день)',
        'when': lambda ans: ans.get('hist'),
        'validate': validate_date_str
    }


]

answer = prompt(main_question, style=custom_style_2)
pprint(answer)


if answer.get('theme') == display_graph \
    and answer.get('period') == all_period:
    fields = answer.get('fields', [])
    draw_graph(fields, 'all')
elif answer.get('theme') == display_graph \
    and answer.get('period') == choose_period:
    fields = answer.get('fields', [])
    period = (answer.get('start_period'), answer.get('end_period'))
    draw_graph(fields, period)
elif answer.get('theme') == display_clean \
    and answer.get('clean_vis'):
    draw_clean(answer.get('clean_vis'))
elif answer.get('theme') == display_hist \
    and answer.get('hist'):
    draw_hist(answer.get('hist'))


