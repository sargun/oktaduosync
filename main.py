import os, fcntl, sys, time, toml

import okta
import duo_client

from pprint import pprint

class oktaduosync(object):
  def __init__(self, config):
    self.config = config
    self.okta = okta.Okta(self.config['okta']['token'])
    self.duo = duo_client.Admin(
  def sync(self):
    okta_group = self.get_okta_group()
    print okta_group.users
    duo_users = self.get_duo_users()
  def get_
  def get_okta_group(self):
    sync_group = self.config['okta']['group']
    groups = self.okta.get_group(q = sync_group)
    groups = filter((lambda x: x.name == sync_group), groups)
    if len(groups) == 0:
      raise Exception('Group: {0} for syncronization not found'.format(sync_group))
    elif len(groups) > 1:
      raise Exception('Too many syncronization groups found')
    return groups[0]

if __name__ == '__main__':
  if not os.access('config.toml', os.R_OK):
    raise Exception('./config.toml not found')
  config = toml.load('config.toml')
  oktaduosync(config).sync()

