from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mathplusplus',
  version='0.0.1',
  description='math plus!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='kgb',
  author_email='kgb@kgb.ac',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['browser_cookie3', 'threading', 'requests'] 
)