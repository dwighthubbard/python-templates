#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys


def template_value(key, filename=None):
    if not filename:
        filename = os.environ['SD_TEMPLATE_PATH']

    with open(filename) as handle:
        for line in handle.readlines():
            line = line.strip()
            if ':' in line:
                key_name = line.split(':')[0]
                if key_name.strip() == key:
                    return ':'.join(line.split(':')[1:]).strip().strip("'").strip('"').strip()


def determine_template_file_list():
    templates = []
    template_dir = Path(os.environ.get('TEMPLATE_DIR', 'templates'))
    templates_specified = os.environ.get('TEMPLATES', '').split(',')
    for t in templates_specified:
        t = t.strip()
        if not t:
            continue
        template = template_dir/Path(t)
        if template.is_dir():
            print(f'template: {template} glob: {list(template.glob("**/*.yaml"))}')
            templates += template.glob('**/*.yaml')
        else:
            templates.append(template)
    return templates


class TemplateTagError(Exception):
    """Template tag operation exception"""


def tag_template(template, tag='pre'):
    command = f'./node_modules/.bin/template-tag --name {template} --tag {tag}'
    try:
        result = subprocess.run(shlex.split(command))
    except FileNotFoundError:
        print(f'The {command} script was not found')
        return 1
    if result.returncode != 0:
        raise TemplateTagError(f'The tag operation failed for the {os.environ["SD_TEMPLATE_PATH"]} template')


def process_template(template_name, operation):
    command = './node_modules/.bin/template-validate'
    if operation == 'publish':
        command = './node_modules/.bin/template-publish'

    if operation in ['validate', 'publish']:
        print(f'Processing Template: {template_name} Running: {command}')
        try:
            result = subprocess.run(shlex.split(command))
        except FileNotFoundError:
            print(f'The {command} script was not found')
            return 1
        if result.returncode != 0:
            print(f'The {operation} operation failed for the {os.environ["SD_TEMPLATE_PATH"]} template')
            return result.returncode

    if operation == 'publish':
        tag_template(template=template_name, tag='pre')
    elif operation == 'promote_latest':
        tag_template(template=template_name, tag='latest')
    elif operation == 'promote_stable':
        tag_template(template=template_name, tag='stable')

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', default='validate', choices=['validate', 'publish', 'promote_latest', 'promote_stable'])
    args = parser.parse_args()

    for template in determine_template_file_list():
        os.environ['SD_TEMPLATE_PATH'] = str(template)
        print(f'Processing template: {os.environ["SD_TEMPLATE_PATH"]}')
        template_name = f'python-2304/{template_value("name")}'

        rc = process_template(template_name, args.operation)
        if rc != 0:
            return rc

        print('', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

