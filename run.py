#!/bin/python

import ConfigParser
import logging
import os
from py2gpio.gpio import ChannelManager

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logging.info('Initializing...')

# Read configuration
config_file = os.getenv('PY2GPIO_CONFIG', 'config.ini')
logging.info('Using configuration "%s" ...' % config_file)
config = ConfigParser.SafeConfigParser()
config.readfp(open(config_file))

# Set debug logging level regarding the configuration
if config.getboolean('general', 'debug'):
    logging.getLogger().setLevel(logging.DEBUG)

# Loading channels
channel_file = os.getenv('PY2GPIO_CHANNEL', 'channels.ini')
logging.info('Loading channels from "%s" ...' % channel_file)
channel = ConfigParser.SafeConfigParser()
channel.readfp(open(channel_file))
manager = ChannelManager(config, channel)

logging.info('Initialized')

try:
  while True:
    continue
except KeyboardInterrupt:
  logging.info('Stopping...')
  manager.stop()
  logging.info('Stopped')
