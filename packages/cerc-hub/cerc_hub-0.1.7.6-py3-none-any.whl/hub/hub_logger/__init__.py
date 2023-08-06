import logging as logger
from pathlib import Path
import os

log_dir = (Path(__file__).parent.parent / 'logs').resolve()
log_file = (log_dir / 'hub.log').resolve()
try:
  if not os.path.isfile(log_file):
    os.mkdir(log_dir)
    with open(log_file, 'x'):
      pass
  logger.basicConfig(filename=log_file, format="%(asctime)s:%(levelname)s:{%(pathname)s:%(funcName)s:%(lineno)d} "
                                               "- %(message)s", level=logger.DEBUG)
except IOError as err:
  print(f'I/O exception: {err}')
