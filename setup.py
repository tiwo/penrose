# -*- coding: utf-8 -*-

import setuptools

with open('README.rst') as readme_rst:
    readme = readme_rst.read()

with open('LICENSE.txt') as license_txt:
    license = license_txt.read()

classifiers=[
    'Programming Language :: Python',
    'Development Status :: 4 - Beta',
    ]

def setup():
    setuptools.setup(
        name='penrose',
        version='0.0.1',
        description='Penrose tilings',
        long_description=readme,
        author='Tiwo',
        author_email='tiwocode@gmail.com',
        url='https://github.com/tiwo/penrose',
        license=license,
        packages=['penrose'],
        classifiers=classifiers,
        )

if __name__ == '__main__':
    setup()
