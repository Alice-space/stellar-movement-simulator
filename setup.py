'''
@Author: Alicespace
@Date: 2019-12-22 20:57:15
@LastEditTime : 2019-12-26 05:58:48
'''
if __name__ == '__main__':
    from setuptools import setup

    setup(name="StellarMovementSimulator",
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
                      'StellarMovementSimulator': 'main.py',
                  },
                  'platforms':
                  {
                      'manylinux1_x86_64',
                      'win_amd64',
                      'macosx_10_6_x86_64',
                  },
                  'plugins': [
                      'pandagl',
                  ],
              }
          })
