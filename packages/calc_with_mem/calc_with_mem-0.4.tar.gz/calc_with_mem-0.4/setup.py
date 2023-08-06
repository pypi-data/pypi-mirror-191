from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='calc_with_mem',
    version='0.4',
    description='Package of a calculator using an internal memory',
    author='Kestutis Gadeikis',
    author_email='kestutis.gadeikis@gmail.com',
    packages=['calc_with_mem', 'tests'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    zip_safe=False)