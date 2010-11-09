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
from django.utils import simplejson as json


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

    fetched = urlfetch.fetch("http://api.twitter.com/1/statuses/user_timeline.json?screen_name="+tweets.username+"&count=200")
    statustext = json.loads(fetched.content)
    
    tweets1 = []
    for tweetInfo in statustext:
	  tweets1.append(tweetInfo["text"])
    
    tweets2 = '<br><br>'.join(tweets1)

    
    content_values = {
        'status': tweets2,
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
