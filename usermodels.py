from google.appengine.ext import db

class Credentials(db.Model):
  username = db.StringProperty()
  password = db.StringProperty()
  active = db.BooleanProperty()
  #account = db.ReferenceProperty(Accounts)


class Accounts(db.Model):
  #credentials = db.ReferenceProperty(Credentials)
  account_name = db.StringProperty()
  #esns = db.ListProperty()
