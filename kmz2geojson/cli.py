import click

import kmzmunger.main as m
import kml2geojson as k2g


@click.command(short_help="Convert KML to GeoJSON")
@click.option('-f', '--separate-folders', is_flag=True,
  default=False)
@click.option('-st', '--style-type', type=click.Choice(k2g.STYLE_TYPES),
  default=None)
@click.option('-sf', '--style-filename',
  default='style.json')
@click.argument('kmz_path')
@click.argument('output_dir')
def kmz2g(kmz_path, output_dir, separate_folders, style_type,
  style_filename):
    """
    Given a path to a KML file, convert it to a a GeoJSON FeatureCollection file and save it to the given output directory.

    If ``--separate_folders``, then create several GeoJSON files, one for each folder in the KML file that contains geodata or that has a descendant node that contains geodata.
    Warning: this can produce GeoJSON files with the same geodata in case the KML file has nested folders with geodata.

    If ``--style_type`` is specified, then also build a JSON style file of the given style type and save it to the output directory under the file name given by ``--style_filename``.
    """
    m.kmz_convert(kmz_path, output_dir, separate_folders, style_type, style_filename)

if __name__ == '__main__':
    kmz2g()