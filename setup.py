from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='kmz2geojson',
    version='0.0.1',
    author='Charles Vardeman',
    url='https://github.com/njcoast/kmz2geojson',
    data_files = [('', ['LICENSE.txt'])],
    description='A Python 3.4 package to convert KMZ files to GeoJSON files',
    long_description=readme,
    license=license,
    install_requires=[
        'click>=6.6',
        'kml2geojson>=4.0.2',
    ],
    entry_points = {
        'console_scripts': ['kmz2g=kmz2geojson.cli:kmz2g'],
    },
    packages=find_packages(exclude=('tests', 'docs')),
)
