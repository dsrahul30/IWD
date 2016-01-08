try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='IWD',
    version='0.1.0',
    author='Duvvuri Surya Rahul',
    author_email='dsrahul@outlook.com',
    packages=['IWD', 'IWD.test'],
    url='http://pypi.python.org/pypi/IWD/',
    license='LICENSE.txt',
    description='Intelligent Water Drops Algorithm for TSP.',
    long_description=open('README.txt').read(),
    install_requires=[
		"argparse >= 1.2.1"		
    ],
)
