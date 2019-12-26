'''
@Author: Alicespace
@Date: 2019-12-22 20:57:15
@LastEditTime : 2019-12-26 06:01:42
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
                      'macosx_10_6_x86_64',
                                    },
                  'plugins': [
                      'pandagl',
                  ],
              }
          })
'''win_amd64,manylinux1_x86_64
                      macosx_10_6_x86_64,
    '''