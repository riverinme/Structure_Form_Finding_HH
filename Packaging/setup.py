from setuptools import setup
setup(name='TwoD_Form_Finding',
      version='1.0.4',
      description='A tool for building structure form-finding',
      author='HH',
      author_email='river_in_me@qq.com',
      license='MIT',
      keywords='form-finding',
      py_modules=['TwoD_Form_Finding'],
      install_requires=['numpy>=1.20.2',
                        'comtypes>=1.1.9', 'matplotlib>=3.4.1'],
      python_requires='>=3.8.0'
      )
