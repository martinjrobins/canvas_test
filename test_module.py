import logging
from canvas_api import regenerate_module

logging.basicConfig(filename='test_module.log', level=logging.DEBUG)

COURSE_NAME = "Software Engineering"
MODULE_NAME = "Test Content"
MODULE_ITEMS = [
    {
        'title': 'Lecture 1',
        'type': 'ExternalURL',
        'external_url': 'https://www.youtube.com/watch?v=VQRuoCawevE',
    },
    {
        'title': 'Exercises 1',
        'type': 'ExternalURL',
        'external_url': 'https://sabs-r3.github.io/module01_se_day1/',
        'sub_items': [
            {
                'title': 'Exercise 1.1',
                'type': 'ExternalURL',
                'external_url': 'https://sabs-r3.github.io/module01_se_day1/',
            },
            {
                'title': 'Exercise 1.2',
                'type': 'ExternalURL',
                'external_url': 'https://sabs-r3.github.io/module01_se_day1/',
            },
            {
                'title': 'Exercise 1.3',
                'type': 'ExternalURL',
                'external_url': 'https://sabs-r3.github.io/module01_se_day1/',
            },
        ]
    },
]

regenerate_module(COURSE_NAME, MODULE_NAME, MODULE_ITEMS)



