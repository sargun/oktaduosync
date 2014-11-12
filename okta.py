__author__ = 'sdhillon'
import requests

from pprint import pprint
class Okta(object):
  def __init__(self, token):
    self.token = token
    self.headers = {'Authorization': 'SSWS {0}'.format(token), 'Accept': 'application/json'}
  def get_group(self, q = None):
    URL = 'https://xactly.okta.com/api/v1/groups'
    if q:
      response = self.get_link(URL, params = {'q': q})
    else:
      response = self.get_link(URL)
    return map((lambda x: Group(self, x)), response)

  def get_link(self, URL, params={}, headers = {}):
    headers.update(self.headers)
    response = requests.get(URL, headers = headers, params = params)
    return response.json()


class Group(object):
  def __init__(self, okta, group):
    self.okta = okta
    self.group = group
  @property
  def name(self):
    return self.group['profile']['name']
  @property
  def users(self):
    user_link = self.group['_links']['users']['href']
    return map((lambda x: User(self.okta, x)), self.okta.get_link(user_link))
  def __repr__(self):
    return '<okta.Group: "{0}">'.format(self.name)

class User(object):
  def __init__(self, okta, user):
    self.okta = okta
    self.user = user

  @property
  def name(self):
    return self.user['profile']['login']
  def __repr__(self):
    return '<okta.User: "{0}">'.format(self.name)

