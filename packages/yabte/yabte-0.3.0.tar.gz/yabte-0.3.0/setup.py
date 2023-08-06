# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yabte', 'yabte.backtest', 'yabte.portopt', 'yabte.utilities']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.2,<2.0.0', 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'yabte',
    'version': '0.3.0',
    'description': 'Yet another backtesting engine',
    'long_description': '# yabte - Yet Another BackTesting Engine\n\nPython module for backtesting trading strategies.\n\nSupport event driven backtesting, ie `on_open`, `on_close`, etc. Also supports multiple assets.\n\nVery basic statistics like book cash, mtm and total value. Currently, everything else needs to be deferred to a 3rd party module like `empyrical`.\n\nThere are some basic tests but use at your own peril. It\'s not production level code.\n\n## Core dependencies\n\nThe core module uses pandas and scipy.\n\n## Installation\n\n```bash\npip install yatbe\n```\n\n## Usage\n\nBelow is an example usage (the performance of the example strategy won\'t be good).\n\n```python\nimport inspect\nfrom pathlib import Path\n\nimport pandas as pd\n\nfrom yabte.backtest import Strategy, StrategyRunner, Order, Book\nfrom yabte.utilities.strategy_helpers import crossover\n\ndata_dir = Path(inspect.getfile(Strategy)).parents[2] / "tests/data/nasdaq"\n\nclass SMAXO(Strategy):\n    def init(self):\n        # enhance data with simple moving averages\n\n        p = self.params\n        days_short = p.get("days_short", 10)\n        days_long = p.get("days_long", 20)\n\n        close_sma_short = (\n            self.data.loc[:, (slice(None), "Close")]\n            .rolling(days_short)\n            .mean()\n            .rename({"Close": "CloseSMAShort"}, axis=1, level=1)\n        )\n        close_sma_long = (\n            self.data.loc[:, (slice(None), "Close")]\n            .rolling(days_long)\n            .mean()\n            .rename({"Close": "CloseSMALong"}, axis=1, level=1)\n        )\n        self.data = pd.concat(\n            [self.data, close_sma_short, close_sma_long], axis=1\n        ).sort_index(axis=1)\n\n    def on_close(self):\n        # create some orders\n\n        for symbol in ["GOOG", "MSFT"]:\n            df = self.data[symbol]\n            ix_2d = df.index[-2:]\n            data = df.loc[ix_2d, ("CloseSMAShort", "CloseSMALong")].dropna()\n            if len(data) == 2:\n                if crossover(data.CloseSMAShort, data.CloseSMALong):\n                    self.orders.append(Order(asset_name=symbol, size=-100))\n                elif crossover(data.CloseSMALong, data.CloseSMAShort):\n                    self.orders.append(Order(asset_name=symbol, size=100))\n\n\n# load some data\nasset_meta = {"GOOG": {"denom": "USD"}, "MSFT": {"denom": "USD"}}\n\ndf_goog = pd.read_csv(data_dir / "GOOG.csv", index_col=0, parse_dates=[0])\ndf_goog.columns = pd.MultiIndex.from_tuples([("GOOG", f) for f in df_goog.columns])\n\ndf_msft = pd.read_csv(data_dir / "MSFT.csv", index_col=0, parse_dates=[0])\ndf_msft.columns = pd.MultiIndex.from_tuples([("MSFT", f) for f in df_msft.columns])\n\n# create a book with 100000 cash\nbook = Book(name="PrimaryBook", cash="100000")\n\n# run our strategy\nsr = StrategyRunner(\n    data=pd.concat([df_goog, df_msft], axis=1),\n    asset_meta=asset_meta,\n    strat_classes=[SMAXO],\n    books=[book],\n)\nsr.run()\n\n# see the trades or book history\nth = sr.trade_history\nbch = sr.book_history.loc[:, (slice(None), "cash")]\n\n# plot the trades against book value\nbvh = sr.book_history.loc[:, (slice(None), "value")].droplevel(axis=1, level=1)\nax = bvh.plot(title="Book Value History")\n\nfor symbol, scol, lcol in [("GOOG", "red", "green"), ("MSFT", "blue", "yellow")]:\n    long_ix = th.query(f"asset_name == \'{symbol}\' and quantity > 0").ts\n    short_ix = th.query(f"asset_name == \'{symbol}\' and quantity < 0").ts\n    bvh.loc[long_ix].rename(columns={"PrimaryBook": f"{symbol} Short"}).plot(color=scol, marker="v", markersize=5, linestyle="None", ax=ax)\n    bvh.loc[short_ix].rename(columns={"PrimaryBook": f"{symbol} Long"}).plot(color=lcol, marker="^", markersize=5, linestyle="None", ax=ax)\n\n```\n\n![Output from code](./readme_image.png)\n\n## Examples\n\nJupyter notebook examples can be found under the [notebooks folder](https://github.com/bsdz/yabte/tree/main/notebooks).\n\n## Documentation\n\nDocumentation can be found on [Read the Docs](https://yabte.readthedocs.io/en/latest/).\n',
    'author': 'Blair Azzopardi',
    'author_email': 'blairuk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bsdz/yabte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
