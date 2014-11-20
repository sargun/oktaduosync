import duo_client

class Duo(object):
  def __init__(self, config):
    self.duo = duo_client.Admin(config['integration_key'], config['secret_key'], config['hostname'])

  def get_users(self):
    return map((lambda x: DuoUser(self, x)), self.duo.get_users())

class DuoUser(object):
  def __init__(self, duo, user):
    self.duo = duo
    self.user = user
  @property
  def username(self):
    return self.user['username']
  def __repr__(self):
    return '<duo.DuoUser: "{0}">'.format(self.username)
  @property
  def email(self):
    return self.user['email']
  def json(self):
    return self.user
  @property
  def user_id(self):
    return self.user['user_id']