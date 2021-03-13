from urllib.parse import urlencode
from urllib.request import urlopen, Request
import json
import datetime
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

  def get_datapoints(self, username, goalname, sort=None, page=None, per=None, count=None):
    url = "%s/users/%s/goals/%s/datapoints.json" % (self.base_url, username, goalname)
    params = {
        'auth_token': self.auth_token,
        'page': page,
        'per': per,
        'count': count,
        'sort': sort,
        }

    result = self.call_api(url, params, 'GET')
    datapoints = json.loads(result)
    return datapoints

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

  def update_datapoint(self, username, goalname, point_id, value, timestamp, daystamp=None, comment=None):
    url = "%s/users/%s/goals/%s/datapoints/%s.json" % (self.base_url, username, goalname, point_id)
    params = {
        'auth_token': self.auth_token,
        'value': value,
        'timestamp': timestamp,
        'daystamp': daystamp,
        'comment': comment,
        }

    result = self.call_api(url, params, 'PUT')
    return result

  def get_datapoint_with_daystamp(self, username, goalname, daystamp):
    """
    Fetch the datapoint with the given daystamp. If there are multiple, return the one with highest ID.
    """
    assert(type(daystamp) == datetime.date)
    daystamp_str = '%04d%02d%02d' % (daystamp.year, daystamp.month, daystamp.day) # This is the format of fetched daystamps
    datapoints = self.get_datapoints(username, goalname, sort='timestamp')

    for datapoint in datapoints[::-1]: # Iterate in reverse order, so we fetch the one with highest ID
      if 'daystamp' not in datapoint:
        continue
      if datapoint['daystamp'] == daystamp_str:
        return datapoint
    return None

  def create_day_datapoint(self, username, goalname, value, daystamp, comment=None, requestid=None):
    return self.create_datapoint(username, goalname, value, daystamp=daystamp, comment=comment, requestid=requestid)

  def set_day_datapoint(self, username, goalname, value, daystamp, comment=None, requestid=None):
    """
    Checks for a datapoint with the given datestamp. If one is found, update it to have given value
    and comment. Otherwise, create a new datapoint with given daystamp, value, and comment.
    Returns (whether a new datapoint was created, results of query)
    """
    to_replace = self.get_datapoint_with_daystamp(username, goalname, daystamp)
    if to_replace is None:
      return (True, self.create_datapoint(username, goalname, value, daystamp=daystamp, comment=comment, requestid=requestid))
    else:
      timestamp = datetime.datetime.combine(daystamp, datetime.datetime.min.time())
      return (False, self.update_datapoint(username, goalname, to_replace['id'], value, timestamp=timestamp, comment=comment))

  def set_goal_aggday(self, username, goalname, new_aggday):
      url = "%s/users/%s/goals/%s.json" % (self.base_url, username, goalname)
      params = {
              'auth_token': self.auth_token,
              'aggday': new_aggday,
              }
      return self.call_api(url, params, 'PUT')

  def get_goals(self, username):
      url = "%s/users/%s/goals" % (self.base_url, username)
      result = self.call_api(url, {'auth_token': self.auth_token}, 'GET')
      return json.loads(result)

  def get_goal_names(self, username):
      goals = self.get_goals(username)
      return [goal['slug'] for goal in goals]

  def call_api(self, url, params, method='GET'):
    pruned_params = {k: v for (k, v) in params.items() if v is not None}
    encoded_params = urlencode(pruned_params).encode('utf-8')

    req = Request(url, encoded_params, method=method)
    response = urlopen(req)

    result = response.read()
    return result
