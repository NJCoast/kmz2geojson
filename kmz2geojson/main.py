import os
import shutil
import xml.dom.minidom as md
import re
from pathlib import Path, PurePath
import json
from lxml import html

from kml2geojson import build_layers, build_feature_collection, disambiguate, to_filename, STYLE_TYPES
from zipfile import ZipFile


def kmz_convert(kmz_path, output_dir, separate_folders=False,
  style_type=None, style_filename='style.json'):
    """
    Given a path to a KML file, convert it to one or several GeoJSON FeatureCollection files and save the result(s) to the given output directory.
    If not ``separate_folders`` (the default), then create one GeoJSON file.
    Otherwise, create several GeoJSON files, one for each folder in the KML file that contains geodata or that has a descendant node that contains geodata.
    Warning: this can produce GeoJSON files with the same geodata in case the KML file has nested folders with geodata.
    If a ``style_type`` is given, then also build a JSON style file of the given style type and save it to the output directory under the name given by ``style_filename``.
    """
    # Create absolute paths
    kmz_path = Path(kmz_path).resolve()
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    output_dir = output_dir.resolve()



    # opening the zip file in READ mode
    with ZipFile(kmz_path, 'r') as zip:
        names = zip.namelist()
        # Find the KML file in the archive
        # There should be only one KML per KNZ
        for name in names:
            if '.kml' in name:
                kml_file = name

        kml_str = zip.read(kml_file)
    # Parse KML
    root = md.parseString(kml_str)

    # Build GeoJSON layers
    if separate_folders:
        layers = build_layers(root)
    else:
        layers = [build_feature_collection(root, name=kmz_path.stem)]

    # Handle HTML Description Tables
    for layer in layers:
        for feature in layer['features']:
            if "<table>" in feature['properties']['description']:
                tree = html.fromstring(feature['properties']['description'])
                
                feature['properties']['date'] = tree.xpath('//table/tr[3]/td/text()')[0].strip()
                feature['properties']['location'] = tree.xpath('//table/tr[5]/td/b/text()')[0].strip()
                feature['properties']['pressure'] = tree.xpath('//table/tr[7]/td/text()')[0].strip().split(" ")[0]
                feature['properties']['speed'] = tree.xpath('//table/tr[9]/td/text()')[0].strip().split(";")[2].strip().replace(" kph", "")

                del feature['properties']['name']
                del feature['properties']['styleUrl']
                del feature['properties']['description']

    # Create filenames for layers
    filenames = disambiguate(
      [to_filename(layer['name'])
      for layer in layers])
    filenames = [name + '.geojson' for name in filenames]

    # Write layers to files
    for i in range(len(layers)):
        path = output_dir/filenames[i]
        with path.open('w') as tgt:
            json.dump(layers[i], tgt, indent = 2)

    # Build and export style file if desired
    if style_type is not None:
        if style_type not in STYLE_TYPES:
            raise ValueError('style type must be one of {!s}'.format(
              STYLE_TYPES))
        builder_name = 'build_{!s}_style'.format(style_type)
        style_dict = globals()[builder_name](root)
        path = output_dir/style_filename
        with path.open('w') as tgt:
            json.dump(style_dict, tgt, indent=2)