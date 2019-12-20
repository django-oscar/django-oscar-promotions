#!/usr/bin/env python
from setuptools import find_packages, setup

from oscar_promotions import VERSION

setup(
    name='django-oscar-promotions',
    version=VERSION,
    url='https://github.com/oscaro/django-oscar-promotins',
    author='Oscar Team',
    author_email='sasha@metaclass.co',
    description='Promotions for Django Oscar',
    long_description=open('README.rst').read(),
    license='BSD',
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=['django>=1.11,<2.3', 'django-oscar>=2.0'],
)
