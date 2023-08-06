from setuptools import setup, find_packages
import os

# define dependencies (requirements) that need to be installed with your package
dependencies = []
rtd_build_env = os.environ.get('READTHEDOCS', False)
if not rtd_build_env:
    dependencies.append('numpy')
# BELOW IS THE EXAMPLE HOW TO ADD DEPENDENCIES AND THEIR SPECIFIC VERSIONS TO YOUR PACKAGE IF NECESSARY
'''
if not rtd_build_env:
    dependencies.append('numpy')
    dependencies.append('pandas')
    dependencies.append('xgboost')
    dependencies.append('scikit-learn>=0.23.2,<=1.1.3')
    dependencies.append('lightgbm>=3.3.0,<=3.3.2')
    dependencies.append('optuna>=2.10.0,<=3.0.4')
    dependencies.append('plotly>=5.3.1,<=5.11.0')
    dependencies.append('matplotlib')
    dependencies.append('python-dateutil>=2.8.1,<=2.8.2')
    dependencies.append('holidays==0.11.3.1')
    dependencies.append('mlxtend')
    dependencies.append('tensorflow>=2.6.0,<=2.11.0')
    dependencies.append('keras>=2.6.0,<=2.11.0')
    dependencies.append('category_encoders>=2.4.0,<=2.5.1')
'''

# PARSE ARGUMENTS FOR setup() FUNCTION
# parse __version__ from version.py
exec(open('boilerplatecode/version.py').read())

# parse long_description from README.rst
with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
  name = 'boilerplatecode',
  packages = find_packages(),
  version = __version__,
  license='MIT',
  description = "Productivity tools to make a developer's life easier",
  long_description=long_description,
#  long_description_content_type="text/markdown",
  author = 'Author Name (your name)',
  author_email = 'author@email.com',
  url = 'https://github.com/DanilZherebtsov/boilerplatecode',   # url of your github repository or to your website
  download_url = 'https://github.com/DanilZherebtsov/boilerplatecode/archive/refs/tags/1.0.0.tar.gz',
  keywords = ['password', 'generate', 'password generator', 'productivity', 'tools', '...'],
  install_requires=dependencies,
  classifiers=[
  'Development Status :: 4 - Beta', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
  'Intended Audience :: Developers',
  'Topic :: Software Development :: Build Tools',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.4',
  'Programming Language :: Python :: 3.5',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Programming Language :: Python :: 3.9',
  'Programming Language :: Python :: 3.10'
  ]
)
