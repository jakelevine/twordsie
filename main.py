#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import sys
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Tweets(db.Model):
    username = db.StringProperty(multiline=False)


class MainHandler(webapp.RequestHandler):
  def get(self):


    template_values = {  
    }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Statuspage(webapp.RequestHandler):
  def post(self):
    tweets = Tweets()
    tweets.username = self.request.get('username')

    fetched = urlfetch.fetch("http://api.twitter.com/1/statuses/user_timeline.json?screen_name="+tweets.username+"&count=5")
    statustext = fetched.content

    loc1st = statustext.find('"text":"')
    status1a = statustext[loc1st+8:]
    loc1end = status1a.find('"},')
    status1b = status1a[:loc1end-2]

    loc2st = status1a.find('"text":"')
    status2a = status1a[loc2st+8:]
    loc2end = status2a.find('"},')
    status2b = status2a[:loc2end-2]

    loc3st = status2a.find('"text":"')
    status3a = status2a[loc3st+8:]
    loc3end = status3a.find('"},')
    status3b = status3a[:loc3end-2]

    loc4st = status3a.find('"text":"')
    status4a = status3a[loc4st+8:]
    loc4end = status4a.find('"},')
    status4b = status4a[:loc4end-2]

    loc5st = status4a.find('"text":"')
    status5a = status4a[loc5st+8:]
    loc5end = status5a.find('"},')
    status5b = status5a[:loc5end-2]



    statusfound1 = status1b
    statusfound2 = status2b
    statusfound3 = status3b
    statusfound4 = status4b
    statusfound5 = status5b

    content_values = {
        'status1': statusfound1,
        'status2': statusfound2,
        'status3': statusfound3,
        'status4': statusfound4,
        'status5': statusfound5,
        'username':tweets.username,
        }

    path = os.path.join(os.path.dirname(__file__), 'statuspage.html')
    self.response.out.write(template.render(path, content_values))

application = webapp.WSGIApplication(
                                     [('/', MainHandler),
                                      ('/statuspage',Statuspage)],
                                     debug=True)
	
def main():

  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
