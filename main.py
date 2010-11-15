#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import sys
import os
import re
from google.appengine.ext import db
from django.utils import simplejson as json
from collections import deque, defaultdict
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

class Tweets(db.Model):
	username = db.StringProperty(multiline=False)


class MainHandler(webapp.RequestHandler):
	def get(self):


		template_values = {  
		}

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class Statuspage(webapp.RequestHandler):
	def get(self):
 		#sets up wordcloud
		user = self.request.get('user')	
		tweets = Tweets()
		tweets.username = user
		tweets.put()
			
		fetched = urlfetch.fetch("http://api.twitter.com/1/statuses/user_timeline.json"
								 "?screen_name="+user+"&count=200")
		tweets = json.loads(fetched.content)
		data = {'cols': [{'type': 'string', 'label': 'Tweets'}],
				'rows': [{'c': [{'v': tweet["text"]}]} for tweet in tweets]}

		#sets up table output
		tweetlist = []
		tweets1 = json.loads(fetched.content)
		for tweetInfo in tweets1:
		      tweetlist.append(tweetInfo["text"])
		
		tweets2 = ''.join(tweetlist)
		tweets2 = tweets2.lower()
	
		fullWords = re.split('\W+',tweets2)
		stopWords = set(['doesn','Your''com','The','http','ly','bit','a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although','always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another', 'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',  'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves', 'the'])
		d = defaultdict(int)
		
		for word in fullWords:
			if word not in stopWords and len(word)>3:
				d[word] += 1
		finalFreq = sorted(d.iteritems(), key = lambda t: t[1], reverse = True)

		tweetarr=[]
		for k,v in finalFreq:
			if v>3:
				j = str(v)
				l = '<b></b>'+'The word <b>'+k+'</b> was tweeted '+j+' times'
				tweetarr.append(l)
				
		tweetput = '<br><br>'.join(tweetarr)

		mosttweet = finalFreq[0]
		mosttweet1 = str(mosttweet)
		mtstart = mosttweet1.find("'")
		mtend = mosttweet1.find(",")
		mtput = mosttweet1[mtstart+1:mtend-1]
		

		template_values = {
							'tweet_data': json.dumps(data),
							'user':user,
							'tweetput':tweetput,
							'mosttweet':mtput,
							}
							
		path = os.path.join(os.path.dirname(__file__), 'statuspage.html')
		self.response.out.write(template.render(path, template_values))


def main():
   application = webapp.WSGIApplication(
										[('/', MainHandler),
										('/statuspage', Statuspage)],
										debug=True)
   run_wsgi_app(application)

if __name__ == '__main__':
   main()