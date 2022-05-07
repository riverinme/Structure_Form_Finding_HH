from setuptools import setup


setup(name='TwoD_Form_Finding',
      version='1.0.5',
      description='A tool for building structure form-finding',
      author='HH',
      author_email='river_in_me@qq.com',
      url="https://github.com/riverinme/Structure_Form_Finding_HH",
      license='MIT',
      keywords='form-finding',
      py_modules=['TwoD_Form_Finding'],
      install_requires=['numpy>=1.20.2',
                        'comtypes>=1.1.9', 'matplotlib>=3.4.1'],
      python_requires='>=3.8.0',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Scientific/Engineering :: Physics",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
      ]

      )
