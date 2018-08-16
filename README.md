# eagleSqlTools
Utility to access the EAGLE public database using python. Based on the [original verison](http://icc.dur.ac.uk/Eagle/Database/eagleSqlTools.py) by John Helly. Modified to support Python 3 as well as Python 2.

## Installation:
 - Download via web UI, or `git clone https://github.com/kyleaoman/eagleSqlTools.git`
 - Install dependencies if necessary (see [`setup.py`](https://github.com/kyleaoman/eagleSqlTools/blob/master/setup.py)). 
 - Global install (Linux): 
   - `cd` to directory with [`setup.py`](https://github.com/kyleaoman/eagleSqlTools/blob/master/setup.py)
   - run `sudo pip install -e .` (`-e` installs via symlink, so pulling repository will do a 'live' update of the installation)
 - User install (Linux):
   - `cd` to directory with [`setup.py`](https://github.com/kyleaoman/eagleSqlTools/blob/master/setup.py)
   - ensure `~/lib/python3.6/site-packages` or similar is on your `PYTHONPATH` (e.g. `echo $PYTHONPATH`), if not, add it (perhaps in `.bash_profile` or similar)
   - run `pip install --prefix ~ -e .` (`-e` installs via symlink, so pulling repository will do a 'live' update of the installation)
 - cd to a directory outside the module and launch `python`; you should be able to do `import eagleSqlTools`
 
 ## Usage:

See examples in the [database release paper](https://arxiv.org/abs/1510.01320). Some examples seem to need some slight modification to work under Python 3.