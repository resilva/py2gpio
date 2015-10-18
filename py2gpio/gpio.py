#!/bin/python

import logging
import requests
import string
import RPi.GPIO as GPIO

logging.getLogger("requests").setLevel(logging.WARNING)


class ChannelManager(object):
  def __init__(self, config, channel_config):
    self.config = config
    self.channel_config = channel_config
    self.load_config()

  def load_config(self):
    # Set broadcom pin-numbering scheme
    GPIO.setmode(GPIO.BCM)

    for channel in self.channel_config.sections():
      logging.debug('Loading channel "%s"' % channel)
      config = dict(self.channel_config.items(channel))
      self.setup_channel(channel, config)
      if self.config.getboolean('general', 'send_on_startup'):
        self.on_data(channel)

  def setup_channel(self, channel, config):
    channel = int(channel)

    if config['mode'] == 'IN' or config['mode'] == GPIO.IN:
      mode = GPIO.IN
    elif config['mode'] == 'OUT' or config['mode'] == GPIO.OUT:
      mode = GPIO.OUT
    else:
      mode = GPIO.BOTH

    if config['event'] == 'RISING' or config['event'] == GPIO.RISING:
      event = GPIO.RISING
    elif config['event'] == 'FALLING' or config['event'] == GPIO.FALLING:
      event = GPIO.FALLING
    else:
      event = GPIO.BOTH

    if config['pull_up_down'] == 'PUD_UP':
      pull_up_down = GPIO.PUD_UP
    elif config['pull_up_down'] == 'PUD_DOWN':
      pull_up_down = GPIO.PUD_DOWN
    else:
      pull_up_down = GPIO.PUD_OFF

    GPIO.setup(channel, mode, pull_up_down=pull_up_down)
    GPIO.add_event_detect(channel, event, callback=self.on_data)

  def on_data(self, channel):
    if self.channel_config.has_section(channel):
      config = dict(self.channel_config.items(channel))
      value = GPIO.input(int(channel))
      url = string.Template(self.config.get('api', 'url')).substitute(id=str(config['id']), value=str(value))

      try:
        logging.info('New data sent for channel "%s" with value "%s", sending to %s' % (channel, value, url))
        requests.get(url)
      except requests.exceptions.RequestException as e:
        logging.error('Error when sending data to %s' % (url))

  def stop(self):
    GPIO.cleanup()
