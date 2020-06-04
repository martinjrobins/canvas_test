import os
import requests
import logging

AUTH_TOKEN = os.environ.get('CANVAS_TOKEN')
CANVAS_URL = 'https://canvas.ox.ac.uk'
AUTH_HEADER = {'Authorization': 'Bearer ' + AUTH_TOKEN}

def fetch_course_id(name):
    logging.debug('Fetching course with name {}'.format(name))
    payload = {}
    results = requests.get(CANVAS_URL + '/api/v1/courses',
                           data=payload, headers=AUTH_HEADER)
    results.raise_for_status()
    results = results.json()

    courses = [r for r in results if name in r['name']]

    if len(courses) < 1:
        raise KeyError('could not find course name in:'
                       ' {}'.format([r['name'] for r in results]))

    if len(courses) > 1:
        raise KeyError('found too many courses: {}'.format(
            [r['name'] for r in courses])
        )

    return courses[0]['id']


def search_modules(course_id, name):
    logging.debug('Searching for module in course {} with name {}'.format(
        course_id, name)
    )
    payload = {'search_term': name}
    results = requests.get(CANVAS_URL +
                           '/api/v1/courses/{}/modules'.format(course_id),
                           data=payload, headers=AUTH_HEADER)
    results.raise_for_status()
    modules = results.json()

    return modules


def create_module(course_id, name):
    logging.info('Creating module in course {} with name {}'.format(course_id, name))
    payload = {
        'module[name]': name,
    }
    result = requests.post(CANVAS_URL +
                           '/api/v1/courses/{}/modules'.format(course_id),
                           data=payload, headers=AUTH_HEADER)
    result.raise_for_status()
    module = result.json()

    return module['id']


def delete_module(course_id, module_id):
    logging.info('Deleting module {}'.format(course_id, module_id))
    payload = {}
    result = requests.delete(CANVAS_URL +
                           '/api/v1/courses/{}/modules/{}'.format(course_id, module_id),
                           data=payload, headers=AUTH_HEADER)
    result.raise_for_status()
    module = result.json()

    return module['id']


def add_module_items(course_id, module_id, module_items):
    logging.info('Adding module items {} to module {} in course {}'.format(
        module_items, module_id, course_id)
    )
    for item in module_items:
        add_module_item(course_id, module_id, item)


def add_module_item(course_id, module_id, item, indent=0):
    logging.debug('Adding module item {} to module {} in course {}'.format(
        item, module_id, course_id)
    )
    payload = {}
    for k, v in item.items():
        if k != 'sub_items':
            payload['module_item[{}]'.format(k)] = v
    payload['module_item[indent]'] = indent

    result = requests.post(CANVAS_URL +
                           '/api/v1/courses/{}/modules/{}/items'.format(
                               course_id, module_id
                           ),
                           data=payload, headers=AUTH_HEADER)
    result.raise_for_status()

    if 'sub_items' in item.keys():
        for sub_item in item['sub_items']:
            add_module_item(course_id, module_id, sub_item, indent=indent+1)


def regenerate_module(course_name, module_name, module_items):
    course_id = fetch_course_id(course_name)
    modules = search_modules(course_id, module_name)
    if len(modules) > 1:
        raise RuntimeError('Too many modules matched name!')
    if len(modules) == 1:
        delete_module(course_id, modules[0]['id'])

    module_id = create_module(course_id, module_name)
    add_module_items(course_id, module_id, module_items)
