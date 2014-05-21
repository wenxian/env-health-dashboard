#!/usr/bin/env python

import os
from setuptools import setup
import version



# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='envhealthdashboard',
    version=version.getVersion(),
    packages=['env_health_dashboard', 'env_health_dashboard_site', 'env_health_dashboard_site.settings'],
    include_package_data=True,
    author='Vito Paine',
    author_email='vpaine@shutterfly.com',
    license='Proprietary to Shutterfly, Inc',
    url='https://ignite.shutterfly.com/docs/DOC-5301',
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock',
        'unittest-xml-reporting',
        'django-nose',
    ],
    setup_requires=['nose>=1.0', 'pep8>=1.3'],
    install_requires=[
        'django',
        'django-jenkins',
        'django-bootstrap3',
        'jira-python',
        'six',
        'python-dateutil',
        'jenkinsapi',
        'croniter',
        'pep8',
        'mock',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content', ],)

