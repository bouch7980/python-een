#!/usr/bin/env python

#  Routes
#  /
#

#  Decorators
#  @login_required

import os
import re
import logging

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

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api import users

from usermodels import *  # I'm storing my models in usermodels.py
from EagleEye import *

een = EagleEye()

class MainHandler(webapp2.RequestHandler):
  def get(self, resource=''):
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/")
      admin_url_text = 'Login'

    template_values = {
      'admin_url': admin_url,
      'admin_url_text': admin_url_text
    }

    render_template(self, 'templates/index.html', template_values)

class ImageHandler(webapp2.RequestHandler):
  def get(self, resource=''):
    if resource is not '':
      image = een.get_image(resource)
      if image is not None:
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(een.get_image(resource))

class CredentialHandler(webapp2.RequestHandler):
  def get(self):
    #Check to see if user is an admin, and display correct link
    admin = users.is_current_user_admin()
    if admin:
      admin_url = users.create_logout_url("/")
      admin_url_text = 'Logout'
    else:
      admin_url = users.create_login_url("/")
      admin_url_text = 'Login'

    username = None
    password = None
    active = None
    c = Credentials().all().fetch(1)
    if c:
      #found a record
      for i in c:
        username = i.username
        password = i.password
        active = i.active

    template_values = {
      'username': username,
      'password': password,
      'active': active,
      'admin_url': admin_url,
      'admin_url_text': admin_url_text
    }

    render_template(self, 'templates/credentials.html', template_values)

  def post(self):
    #if users.is_current_user_admin():
    c = Credentials()
    c.username = self.request.get("username")
    c.password = self.request.get("password")
    c.put()

    self.redirect("/credentials")



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
                              ('/image/([^/]+)?', ImageHandler),
                              ('/credentials', CredentialHandler)],
                              debug = is_local())
