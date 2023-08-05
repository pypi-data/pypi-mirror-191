# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databallpy',
 'databallpy.load_data',
 'databallpy.load_data.event_data',
 'databallpy.load_data.tracking_data']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'databallpy',
    'version': '0.1.1',
    'description': 'A package for loading, preprocessing, vizualising and synchronizing soccere event aand tracking data.',
    'long_description': '# databallpy\n\nA package for loading, preprocessing, vizualising and synchronizing soccere event and tracking data.\n\nThis package is developed to create a standardized way to analyse soccer matches using both event- and tracking data. Other packages, like [kloppy](https://github.com/PySport/kloppy) and [floodligth](https://github.com/floodlight-sports/floodlight), already standardize the import of data sources. The current package goes a step further in combining different data streams from the same match. In this case, the `Match` object combines information from the event and tracking data.\n\nWe are currently working on adding more data sources and on creating a `Match.synchronise_tracking_and_event_data()` function to efficiently align all events with a timeframe in the tracking data. This would make it possible to get contextual information from the tracking data at the exact moment that the event is taking place.\n\n## Installation\n\n```bash\n$ pip install databallpy\n```\n\n## Usage\n\nThe package is centered around the `Match` object. A `Match` has tracking data, event data metadata about the match.\n\n```console\n$ from databallpy.match import get_match\n$\n$ match = get_match(\n$   tracking_data_loc="data/tracking_data.dat",\n$   tracking_metadata_loc="data/tracking_metadata.xml",\n$   tracking_data_provider="tracab"\n$   event_data_loc="data/event_data_f24.xml",\n$   event_metadata_loc="data/event_metadata_f7.xml",\n$   event_data_provider="opta",\n$ )\n$ match.home_team_name # the team name of the home playing team\n$ match.away_players # pandas dataframe with the names, ids, shirt numbers and positions of the away team\n$ match.tracking_data # pandas dataframe with tracking data of the match\n$ match.event_data # pandas dataframe with event data of the match\n```\n\nSee [the documentation](https://databallpy.readthedocs.io/en/latest/autoapi/databallpy/match/index.html) of the `Match` object for more options. Note that this package is developed to combine event and tracking data, therefore both datastreams are necessary to create a `Match` object.\n\n## Visualizing\n\nThe packages also provides tools to visualise the data. Note that to save a match clip the package relies on the use of ffmpeg. Make sure to have installed it to your machine and added it to your python path, otherwise the `save_match_clip()` function will produce an error.\n\n```console\n$ from databallpy.match import get_match\n$ from databallpy.visualize import save_match_clip\n$\n$ match = get_match(\n$   tracking_data_loc="data/tracking_data.dat",\n$   tracking_metadata_loc="data/tracking_metadata.xml",\n$   tracking_data_provider="tracab"\n$   event_data_loc="data/event_data_f24.xml",\n$   event_metadata_loc="data/event_metadata_f7.xml",\n$   event_data_provider="opta",\n$ )\n$\n$ save_match_clip(match, start_idx=0, end_idx=100, folder_loc="data", title="example")\n```\n\nThis function will save a .mp4 file in `"data/"` directory of the `match.tracking_data` from index 0 untill index 100.\n\nhttps://user-images.githubusercontent.com/49450063/217216924-748841e3-dddd-4149-a3c5-000320a91865.mp4\n\n## Documentation\n\nThe official documentation can be found [here](https://databallpy.readthedocs.io/en/latest/autoapi/databallpy/index.html).\n\n## Providers\n\nFor now we only have one tracking data and one event data provider. We are planning on adding more providers later on.\n\nEvent data providers:\n- Opta\n\nTracking data providers:\n- Tracab\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`databallpy` was created by Alexander Oonk & Daan Grob. It is licensed under the terms of the MIT license.\n\n## Similar projects\n\nAlthough we think this package helps when starting to analyse soccer data, other packages may be better suited for your specific needs. Make sure to check out the following packages as well:\n- [kloppy](https://github.com/PySport/kloppy)\n- [floodlight](https://github.com/floodlight-sports/floodlight)\n- [codeball](https://github.com/metrica-sports/codeball)\n\nAnd for a more specific toturials on how to get started with soccer data"\n- [Friends of Tracking](https://github.com/Friends-of-Tracking-Data-FoTD)\n\n\n\n',
    'author': 'Alexander Oonk',
    'author_email': 'alexanderoonk26@gmail.com',
    'maintainer': 'Alexander Oonk',
    'maintainer_email': 'alexanderoonk26@gmail.com',
    'url': 'https://pypi.org/project/databallpy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
