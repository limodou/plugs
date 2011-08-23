__doc__ = """
=====================
Plugs Introduction
=====================

:Author: Limodou <limodou@gmail.com>

.. contents:: 

About Plugs
----------------

Plugs is an apps collection project for uliweb. So you can use any app of it
to compose your project.

License
------------

Plugs is released under BSD license. Of cause if there are some third party
apps not written by me(limodou), it'll under the license of itself.

"""

from setuptools import setup

setup(name='plugs',
    version='0.0.1b1',
    description="Apps collection for uliweb",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    packages = ['plugs'],
    platforms = 'any',
    keywords='wsgi web framework',
    author='limodou',
    author_email='limodou@gmail.com',
    url='http://code.google.com/p/plugs',
    license='BSD',
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'uliweb_apps': [
          'helpers = plugs',
        ],
    },
)
