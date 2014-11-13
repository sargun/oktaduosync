
import logging
import duo, okta


logger = logging.getLogger(__name__)

print __name__

class OktaDuoSync(object):
  def __init__(self, config):
    self.config = config
    self.okta = okta.Okta(self.config['okta']['token'])
    self.duo = duo.Duo(self.config['duo'])

  def sync(self):
    okta_group = self.get_okta_group()
    okta_users = okta_group.users
    duo_users = self.get_duo_users()
    self.sync_users(okta_users, duo_users)

  def sync_users(self, okta_users, duo_users):
    logger.info('Beginning user sync')
    okta_user_dict = {}
    duo_user_dict = {}
    for i in okta_users:
      okta_user_dict[i.email] = i
    for i in duo_users:
      duo_user_dict[i.email] = i

    #Users that exist in okta, that don't exist in duo
    users_to_add = set(okta_user_dict.keys()) - set(duo_user_dict.keys())

    #Users to delete
    users_to_del = set(duo_user_dict.keys()) - set(okta_user_dict.keys())

    for key in users_to_add:
      self.add_user(okta_user_dict[key])
    for key in users_to_del:
      self.del_user(duo_user_dict[key])
    print  okta_user_dict,  duo_user_dict
    print users_to_add, users_to_del

  def del_user(self, duo_user):
    self.duo.duo.delete_user(duo_user.user_id)

  def add_user(self, okta_user):
    print okta_user
    self.duo.duo.add_user(okta_user.prefix,
                          realname = okta_user.realname,
                          email = okta_user.email)

  def get_duo_users(self):
    return self.duo.get_users()
  def get_okta_group(self):
    sync_group = self.config['okta']['group']
    groups = self.okta.get_group(q = sync_group)
    groups = filter((lambda x: x.name == sync_group), groups)
    if len(groups) == 0:
      raise Exception('Group: {0} for syncronization not found'.format(sync_group))
    elif len(groups) > 1:
      raise Exception('Too many syncronization groups found')
    return groups[0]
