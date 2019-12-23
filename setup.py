'''
@Author: Alicespace
@Date: 2019-12-22 20:57:15
@LastEditTime : 2019-12-23 08:48:25
'''
from setuptools import setup

setup(name="Stellar Movement Simulator",
      options={
          'build_apps': {
              'optimized_wheel_index': 'https://pypi.org/simple/',
              'include_patterns': [
                  'res/**',
              ],
              'include_modules': {
                  '*': [
                      'scipy.special._ufuncs_cxx',
                      'scipy.linalg.cython_blas',
                      'scipy.linalg.cython_lapack',
                      'scipy.sparse.csgraph._validation',
                      'scipy._lib.messagestream',
                  ],
              },
              'gui_apps': {
                  'Stellar Movement Simulator': 'main.py',
              },
              'plugins': [
                  'pandagl',
              ],
          }
      })