from setuptools import setup, find_packages
import sys, os

setup(name='failureaction',
      version="1.0a1",
      description="Decorators for actions executed in case of an exception",
      long_description=open('README.txt').read(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      keywords='Exception Decorator Zope',
      author='Tom Gross',
      author_email='itconsense@gmail.com',
      url='',
      license='ZPL 2.1',
      zip_safe=True,
      test_suite = 'tests.test_suite',
      py_modules=['failureaction']
      )
