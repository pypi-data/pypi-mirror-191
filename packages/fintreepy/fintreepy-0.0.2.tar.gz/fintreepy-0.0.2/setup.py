from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = ''
LONG_DESCRIPTION = ''
 
classifiers = [
  'Development Status :: 2 - Pre-Alpha',
  'Intended Audience :: Financial and Insurance Industry',
  'Operating System :: Microsoft :: Windows',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fintreepy',
  version=VERSION,
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  url='https://github.com/sammuharem/fintreepy',  
  author='Sam Muharem',
  author_email='sj.muharem@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['numpy'] 
)