from setuptools import setup, find_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pecoret_default_templates',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/PeCoReT/default_templates',
    license='',
    author='peco21',
    author_email='',
    include_package_data=True,
    description='PeCoReT default templates.',
    long_description=long_description,
    long_description_content_type='text/markdown')
