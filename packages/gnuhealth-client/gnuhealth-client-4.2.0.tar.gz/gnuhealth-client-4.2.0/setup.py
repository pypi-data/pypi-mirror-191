#!/usr/bin/env python

# SPDX-FileCopyrightText: 2017-2023 Luis Falcón <falcon@gnuhealth.org>
# SPDX-FileCopyrightText: 2017-2023 GNU Solidario <health@gnusolidario.org>

# SPDX-License-Identifier: GPL-3.0-or-later

#########################################################################
#             GNUHEALTH HOSPITAL MANAGEMENT - GTK CLIENT                #
#                     https://www.gnuhealth.org                         #
#########################################################################
#                     setup.py: Setuptools file                         #
#########################################################################
from setuptools import setup, find_packages

long_desc = open('README.rst').read()

version = open('version').read().strip()

name = 'gnuhealth-client'

download_url = 'https://ftp.gnu.org/gnu/health'

setup(
    name=name,
    version=version,
    description='The GNU Health GTK client',
    long_description=long_desc,
    author='GNU Solidario',
    author_email='health@gnusolidario.org',
    url='https://www.gnuhealth.org',
    download_url=download_url,
    keywords='eHealth ERM HMIS LIMS',
    scripts=['bin/gnuhealth-client'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: GTK',
        'Framework :: Tryton',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        ],
    platforms='any',
    license='GPL v3+',
    python_requires='>=3.6,<4',
    install_requires=[
        'pycairo',
        "python-dateutil",
        'PyGObject',
        ],
    extras_require={
        'calendar': ['GooCalendar>=0.7'],
        },
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
