__author__ = "Shantanu H. Joshi"
__copyright__ = "Copyright 2013, Shantanu H. Joshi Ahmanson-Lovelace Brain Mapping Center, \
                 University of California Los Angeles"
__email__ = "s.joshi@ucla.edu"

from setuptools import setup, find_packages

setup(
    name='shapeio',
    version='0.1dev',
    packages=find_packages(),
    license='TBD',
    package_data={'shapeio': ['.gitignore', '.idea']},
    scripts=['bin/convert_curve_format.py',
             'bin/convert_surf_format.py',
             'bin/subtract_surf_attributes.py'],
    # long_description=open('README.txt').read(),
)
