# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osu_data_csv']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'tqdm>=4.64.1,<5.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['osu-data-csv = osu_data_csv.main:main']}

setup_kwargs = {
    'name': 'osu-data-csv',
    'version': '0.1.5',
    'description': 'Downloads and Converts .sqls from data.ppy.sh into .csv',
    'long_description': '# Data PPY CSV Retrieval\n\nRetrieve data from the data ppy dump as CSV files.\n\n# :exclamation: Important\n\nI have been given permission to upload the script, however, not the data. \n\nThus, if **you** want to upload the data elsewhere, please contact ppy through contact@ppy.sh.\n\n```\nAll data provided here is done so with the intention of it being used for statistical analysis\nand testing osu! subsystems.\n\nPermission is NOT implicitly granted to deploy this in production use of any kind.\nShould you wish to publicly use/expose the data provided here, please contact me first at contact@ppy.sh.\n\nPlease see https://github.com/ppy/osu-performance for more information.\n\nThanks,\nppy\n```\n\n## Downloading & Converting\n\n1) `pip install osu-data-csv`\n2) run `osu-data-csv` in the terminal\n    ```bash\n    osu-data-csv\n    ```\n\n    A series of prompts should show up. See **Arguments** below for more info and examples\n\n3) (Alternatively) run in a single command\n\n    ```bash\n    osu-data-csv \\\n      -y "2022_12" \\\n      -d "mania" \\\n      -s "1000" \\\n      -l "data/" \\\n      -c "N" \\\n      -q "Y" \\\n      -i "path/to/ignore_mapping.yaml"\n    ```\n\n## Arguments\n\n| Option           | Option (Shorthand) | Desc.                                                                  | Example                       |\n|------------------|--------------------|------------------------------------------------------------------------|-------------------------------|\n| --year_month     | -y                 | Dataset Year and Month. Will fail if doesn\'t exist anymore             | `2022_10`                     |\n| --mode           | -d                 | Gamemode. [\'catch\', \'mania\', \'osu\', \'taiko\']                           | `mania`                       |\n| --set            | -s                 | Dataset of Top 1K or 10K players. [\'1000\', \'10000\']                    | `1000`                        |\n| --dl_dir         | -l                 | Directory to download to. Best if empty. Can be not created.           | `data/`                       |\n| --cleanup        | -c                 | Whether to delete unused files after conversion. [\'Y\', \'N\']            | `N`                           |\n| --bypass_confirm | -q                 | Whether to bypass confirmation of downloaded and new files. [\'Y\', \'N\'] | `N`                           |\n| --ignore_path    | -i                 | Path to YAML file ignore  specification (see next section)             | `path/to/ignore_mapping.yaml` |\n\nIt\'s set to retrieve the following:\n\n```\nosu_user_stats_<MODE>.sql\nosu_scores_<MODE>_high.sql\nosu_beatmap_difficulty.sql\nosu_beatmaps.sql\n```\n\n### Selecting Columns\n\nIt\'s slow as it converts **all columns**. To speed this up, and reduce space taken, it\'s best to use `--ignore_path` \nwith a YAML file.\n\n1) [Download the template `ignore_mapping.yaml` here](ignore_mapping.yaml) \n2) Comment **out** fields that you want to **include**.\n3) Call `osu-data-csv -i path/to/ignore_mapping.yaml [other options]`\n\nFor example\n```yaml\nosu_beatmap_difficulty.sql:\n#  - beatmap_id\n  - mode\n  - mods\n  - diff_unified\n  - last_update\nosu_beatmaps.sql:\n  - beatmap_id\n  - beatmapset_id\n#  - user_id\n#  - filename\n...\n```\n\nWe\'ll retrieve `beatmap_id` from `osu_beatmap_difficulty.sql` and `user_id`, `file_name` from `osu_beatmaps.sql` \n\n## Output\n\nThis will generate a few files. You\'d want to retrieve the `.csv`.\n\n```\n- main.py \n- <dl_dir>/\n  - 202X_XX_01_performance_<MODE>_top_<SET>.tar.bz2 (*)\n  - 202X_XX_01_performance_<MODE>_top_<SET>/\n    - csv/\n      - osu_user_stats_<MODE>.csv\n      - _.csv\n      - ...\n    - osu_user_stats_<MODE>.sql (*)\n    - _.sql (*)\n    - ...\n```\n\n- `(*)` files are deleted if `cleanup` is enabled.\n',
    'author': 'Eve-ning',
    'author_email': 'dev_evening@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
