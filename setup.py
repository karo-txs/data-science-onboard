#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Karolayne Teixeira da Silva",
    author_email='karolayne.2019230005@unicap.br',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Building a full data-science project end-to-end.",
    entry_points={
        'console_scripts': [
            'data_science_onboard=data_science_onboard.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='data_science_onboard',
    name='data_science_onboard',
    packages=find_packages(include=['data_science_onboard', 'data_science_onboard.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AFKaro/data_science_onboard',
    version='0.1.0',
    zip_safe=False,
)
