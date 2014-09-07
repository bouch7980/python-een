import re, urllib, logging
from google.appengine.api import memcache
from google.appengine.api import urlfetch
import json as simplejson
from google.appengine.ext import db
from usermodels import *  # I'm storing my models in usermodels.py

class EagleEye():

  def __init__(self):
    self.cookie = None
    self.host = "https://apidocs.eagleeyenetworks.com"

  def login(self):
    logging.info('starting login()')
    url = self.host + "/g/aaa/authenticate"
    username = memcache.get('username')
    password = memcache.get('password')

    if not username and not password:
      logging.warning('username and password are not in memcache, pulling latest from datastore')
      c = Credentials().all().fetch(1)
      if c:
        #found a record
        for i in c:
          username = i.username
          password = i.password

    payload = {'username': username, 'password': password}

    result = urlfetch.fetch(url=url,
                            payload=simplejson.dumps(payload),
                            method=urlfetch.POST,
                            headers={'Content-Type': 'application/json'})

    if result.status_code == 200:
      url = self.host + "/g/aaa/authorize"
      payload = {'token': simplejson.loads(result.content)['token']}

      result = urlfetch.fetch(url=url,
                              payload=simplejson.dumps(payload),
                              method=urlfetch.POST,
                              headers={'Content-Type': 'application/json'})

      matches = re.search('videobank_sessionid=([\w]*);', result.headers['set-cookie'])
      self.cookie = matches.group(1)
      memcache.set('auth_token', self.cookie)
      logging.info('done login()')
      return simplejson.loads(result.content)


  def get_auth(self):
    token =  memcache.get('auth_token')
    if token:
      return token
    return None

  def get_image(self, esn, direction='prev'):
    token = self.get_auth()
    if token is not None:
      pattern = self.host + "/asset/%s/image.jpeg?c=%s&t=now&a=pre&A=%s"
      url = pattern % (direction, esn, token)
      logging.info('already have a cookie in memcache, get_image URL: ' + url)
      result = urlfetch.fetch(url=url)
      if result.status_code == 401:
        logging.warning('got a 401 for get_image, calling login')
        self.login()
        self.get_image(esn)
      if result.status_code == 200:
        return result.content
    else:
      logging.info("don't have a cooke in memcache, calling login()")
      self.login()
      self.get_image(esn)
