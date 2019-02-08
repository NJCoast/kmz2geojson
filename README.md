# Command line tool to convert KMZ to GeoJSON for NJcoast

This tool is used to convert [National Huricaine Center GIS](https://www.nhc.noaa.gov/gis/) forecast KMZ format forcast trajectories to the web standard [GeoJSON](http://geojson.org/) for input into NJcoast computational models. The tool depends on the existing [kml2geojson](https://pypi.org/project/kml2geojson/) library, but adds support for decompressing the [kmz](https://developers.google.com/kml/documentation/kmzarchives) to extract the kml files for processing by the kml2geojson library.

## Installation

The tool can be installed using standard python installation tool pip.

## Command line usage

The kmz2geojson tool installs as the command k2g. This k2g command can be called from the command line using:

```shell
$ k2g [OPTIONS] KML_PATH OUTPUT_DIR
```

Where KML_PATH is the path to the kmz file to be converted and OUTPUT_DIR is the directory where the resultant GeoJSON is to be written.

Running the command:

```shell
$ k2g --help
```

Produces a full set of command line arguments that can be used with the tool.

## Development

The tool uses [pipenv](https://pipenv.readthedocs.io/en/latest/) to control virtual environment resources during development. To create a virtual environment for developement using pipenv.

```shell
$ pipenv install --dev
```

The library consists of only 2 files. A command line argument processor using the python [click](https://click.palletsprojects.com) library contained in kmz2geojson/cli.py. Core kmz processing code is in kmz2geojson/main.py.
