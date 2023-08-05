# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['folium_pmtiles']

package_data = \
{'': ['*']}

install_requires = \
['folium>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'folium-pmtiles',
    'version': '0.1.1',
    'description': 'Folium Plugin to Support PMTiles',
    'long_description': '# 🗺️ Folium Plugin to support PMTiles\n\n## Basic usage\n\n### Installation\n\n```\npip install folium folium-pmtiles\n```\n\n### Vector\n\n```python\nimport folium\n\nfrom folium_pmtiles.vector import PMTilesVector\n\nm = folium.Map(location=[43.7798, 11.24148], zoom_start=12, tiles=None)\npmtiles_layer = PMTilesVector(\n    "https://protomaps.github.io/PMTiles/protomaps(vector)ODbL_firenze.pmtiles",\n    "folium_layer_name",\n    options={\n        "attribution": """<a href="https://protomaps.com">Protomaps</a> © <a href="https://openstreetmap.org/copyright">OpenStreetMap</a>\'"""\n    },\n)\nm.add_child(pmtiles_layer)\n```\n\nSee https://github.com/protomaps/protomaps.js/blob/eb9ca41a7469d30beada65f53cd51d94ea77c305/src/frontends/leaflet.ts#L42-L63\nfor valid options\n\n### Raster\n\n```python\nimport folium\n\nfrom folium_pmtiles.raster import PMTilesRaster\n\nm = folium.Map(location=[43.7798, 11.24148], zoom_start=2, tiles=None)\npmtiles_layer = PMTilesRaster(\n    "https://protomaps.github.io/PMTiles/stamen_toner(raster)CC-BY+ODbL_z3.pmtiles",\n    "folium_layer_name",\n    options={\n        "attribution": """Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>."""\n    },\n)\nm.add_child(pmtiles_layer)\n```\n\nsee https://leafletjs.com/reference.html#gridlayer-option for valid options\n\n## Dev Setup\n\n```\npoetry install --with dev\npoetry run pre-commit install\n```\n',
    'author': 'Jt Miclat',
    'author_email': 'jtmiclat@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jtmiclat/folium-pmtiles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
