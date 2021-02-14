from urllib.parse import urlencode
from urllib.request import urlopen, Request
# API details at https://www.beeminder.com/api


class Beeminder:
  def __init__(self, this_auth_token):
    self.auth_token = this_auth_token
    self.base_url = 'https://www.beeminder.com/api/v1'

  def get_user(self, username):
    url = "%s/users/%s.json" % (self.base_url, username)
    params = {'auth_token': self.auth_token}
    result = self.call_api(url, params, 'GET')
    return result

  def get_goal(self, username, goalname):
    url = "%s/users/%s/goals/%s.json" % (self.base_url, username, goalname)
    params = {'auth_token': self.auth_token}

    result = self.call_api(url, params, 'GET')
    return result

  def get_datapoints(self, username, goalname, page=None, per=None, count=None):
    url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url, username, goalname)
    params = {
        'auth_token': self.auth_token,
        'page': page,
        'per': per,
        'count': count,
        }

    result = self.call_api(url, params, 'GET')
    return result

  def create_datapoint(self, username, goalname, value, timestamp=None, daystamp=None, comment=None, requestid=None):
    url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url, username, goalname)
    params = {
        'auth_token': self.auth_token,
        'value': value,
        'timestamp': timestamp,
        'daystamp': daystamp,
        'comment': comment,
        'requestid': requestid,
        }

    result = self.call_api(url, params, 'POST')
    return result

  def call_api(self, url, params, method='GET'):
    pruned_params = {k: v for (k, v) in params.items() if v is not None}
    encoded_params = urlencode(pruned_params).encode('utf-8')
    if method == 'POST':
      req = Request(url, encoded_params)
      response = urlopen(req)
    else:
      response = urlopen(url + '?' + encoded_params)

    result = response.read()
    return result
