from setuptools import find_packages, setup

import os

BASE_DIR = os.path.realpath(os.path.dirname(__file__))
VERSION = '0.4.9'
PACKAGES = [p for p in find_packages() if not p.startswith('tests')]


def parse_requirements():
    reqs = []
    if os.path.isfile(os.path.join(BASE_DIR, 'requirements.txt')):
        with open(os.path.join(BASE_DIR, 'requirements.txt'), 'r') as fd:
            for line in fd.readlines():
                line = line.strip()
                if line:
                    reqs.append(line)
    return reqs


def get_description():
    with open(os.path.join(BASE_DIR, 'README.md'), 'r') as fh:
        return fh.read()


if __name__ == '__main__':
    setup(
        version=VERSION,
        name='la_panic',
        description='iPhone kernel panic parser',
        long_description=get_description(),
        long_description_content_type='text/markdown',
        packages=PACKAGES,
        author='LoboAlpha',
        install_requires=parse_requirements(),
        entry_points={
            'console_scripts': [
                'la_panic=la_panic.__main__:cli'
            ],
        },
        url='https://gitlab.com/yanivhasbanidev/la_panic',
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],
        tests_require=['pytest'],
    )
