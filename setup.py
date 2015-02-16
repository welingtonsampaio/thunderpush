#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'sockjs-tornado==1.0.1',
    'tornado==3.2.2',
    'wsgiref==0.1.2',
    'requests',
    'argparse',
    'pymongo'
]

setup(
    name='thunderpush',
    version='0.9.7',
    author='Krzysztof Jagiello',
    author_email='balonyo@gmail.com',
    description='Tornado and SockJS based, complete Web push solution.',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    license='BSD',
    include_package_data=True,
    url='https://github.com/thunderpush/thunderpush',
    test_suite='thunderpush.tests.suite',
    entry_points={
        'console_scripts': [
            'thunderpush = thunderpush.runner:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
)
