#!/usr/bin/env python

#  Routes
#  /
#  

#  Decorators
#  @login_required

import os

# They are changing Django version, need to include this
# http://code.google.com/appengine/docs/python/tools/libraries.html#Django
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template

import webapp2
import urllib2
import json as simplejson

import wsgiref.handlers, logging
import cgi, time, datetime
#from google.appengine.ext.webapp import template
#from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
#  from google.appengine.ext.webapp.util import login_required
#  from google.appengine.api import users
#  from google.appengine.api import mail
#  from google.appengine.api import memcache
#  from google.appengine.api import taskqueue

from google.appengine.api import memcache
from google.appengine.api import urlfetch


from usermodels import *  #I'm storing my models in usermodels.py


class EagleEye():
  def __init():
    self.cookies = None

  def authenticate(self):
    pass

  def authorize(self):
    pass

  def get_auth(self):
      # get key from memcache
      token = memcache.get('auth_token')

      # go get an Auth token
      if token is not None:
        return token
      else:
        memcache.set('auth_token', '<token>')
        get_auth() 

een = EagleEye()

class MainHandler(webapp2.RequestHandler):
  def get(self, resource=''):
    render_template(self, 'templates/index.html')

class ImageHandler(webapp2.RequestHandler):
  def get(self, resource=''):
    #make the url
    pattern = "https://login.eagleeyenetworks.com/asset/prev/image.jpeg?c=%s&t=now&a=pre&A=%s" 
    url = pattern % (resource, een.get_auth())
   
    # make the request
    result = urlfetch.fetch(url)
   
    # do something with the results
    if result.status_code == 200:
      self.response.headers['Content-Type'] = 'image/jpeg'
      self.response.out.write(result.content)

    if result.status_code == 401:
      pass

    if result.status_code == 403:
      pass


def is_local():
  # Turns on debugging error messages if on local env  
  return os.environ["SERVER_NAME"] in ("localhost")  
    
def render_template(call_from, template_name, template_values=dict()):
  # Makes rendering templates easier.
  path = os.path.join(os.path.dirname(__file__), template_name)
  call_from.response.out.write(template.render(path, template_values))

def render_json(self, data):
  self.response.headers['Content-Type'] = 'application/json'
  self.response.out.write(simplejson.dumps(data))
  


app = webapp2.WSGIApplication([('/', MainHandler),
                              ('/image/([^/]+)?', ImageHandler)],
                              debug = is_local())
