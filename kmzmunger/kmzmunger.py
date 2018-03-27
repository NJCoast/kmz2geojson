import kml2geojson as kml
from zipfile import ZipFile
import xml.dom.minidom as md
from pathlib import Path
import pprint
import json

file_name = "data/AL152017_035Aadv_TRACK.kmz"
separate_folders=False
output_dir = './'
output_dir = Path(output_dir)
kml_path = Path('./').resolve()

# opening the zip file in READ mode
with ZipFile(file_name, 'r') as zip:
    # printing all the contents of the zip file
    data = zip.read("AL152017_035Aadv_TRACK.kml")

root = md.parseString(data)

 # Build GeoJSON layers
if separate_folders:
    layers = kml.main.build_layers(root)
else:
    layers = [kml.main.build_feature_collection(root, name=kml_path.stem)]

# Create filenames for layers
filenames = kml.disambiguate(
    [kml.main.to_filename(layer['name'])
    for layer in layers])
filenames = [name + '.geojson' for name in filenames]

for i in range(len(layers)):
    pprint.pprint(layers[i])

 # Write layers to files
""" for i in range(len(layers)):
    path = output_dir/filenames[i]
    with path.open('w') as tgt:
        json.dump(layers[i], tgt, indent = 1) """