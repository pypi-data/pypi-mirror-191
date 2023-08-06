from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Kashier',
  version='1.0.6',
  description='proxy middleware Kashier api',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kashier Team',
  author_email='mghanem@kashier.io',
  license='MIT', 
  classifiers=classifiers,
  keywords='kashier payment', 
  packages=find_packages(),
  install_requires=['requests'] 
)
