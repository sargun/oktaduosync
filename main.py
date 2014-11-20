import os, fcntl, sys, time, toml

import logging, logging.config
import oktaduosync

from pprint import pprint

logger = logging.getLogger(__name__)

if __name__ == '__main__':
  if not os.access('config.toml', os.R_OK):
    raise Exception('./config.toml not found')
  config = toml.load('config.toml')
  baseConfig = {'version': 1}
  baseConfig.update(config['logging'])
  logging.config.dictConfig(baseConfig)
  oktaduosync.OktaDuoSync(config).sync()

