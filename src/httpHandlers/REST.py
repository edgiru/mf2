from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

from httpHandlers.models import Payment, Tag, Filter, T2p, Vault, User

kind2model = {
	'payment': Payment,
	'tag':     Tag,
	'vault':   Vault,
	't2p':     T2p,
	'filter':  Filter,
}

class RESTfulHandler(webapp.RequestHandler):
	
	def get(self, kind, id):
		
		if kind == 'all':
			result = self.getAllData()
			self.response.out.write(result)
		else:
			
			if not kind in kind2model:
				self.error(500)
				return
		
			result = []
			query = kind2model[kind].all().ancestor(User.current())
			for item in query:
				result.append(item.toDict())
			result = simplejson.dumps(result)
			self.response.out.write(result)

	def post(self, kind, id):
		
		if not kind in kind2model:
			self.error(500)
			return
		
		data = simplejson.loads(self.request.body)
		model = kind2model[kind](parent=User.current())
		model.fromDict(data)
		model.put()
		data = simplejson.dumps(model.toDict())
		self.response.out.write(data)

	def put(self, kind, id):

		if not kind in kind2model:
			self.error(500)
			return
		
		data = simplejson.loads(self.request.body)
		model = kind2model[kind].get_by_id(int(id), parent=User.current())
		model.fromDict(data)
		model.put()
		data = simplejson.dumps(model.toDict())
		self.response.out.write(data)

	def delete(self, kind, id):

		if not kind in kind2model:
			self.error(500)
			return
		
		model = kind2model[kind].get_by_id(int(id), parent=User.current())
		model.delete()
		
	def getAllData(self):
		result = {
			'Vaults': Vault,
			'Filters': Filter,
			'Payments': Payment,
			'T2ps': T2p,
			'Tags': Tag
		}
		
		for i in result.keys():
			query = result[i].all().ancestor(User.current())
			result[i] = []
			for entry in query:
				result[i].append(entry.toDict())
			
		return simplejson.dumps(result)

			
application = webapp.WSGIApplication([('/api/(all|payment|tag|vault|t2p|filter)/?([0-9]*)', RESTfulHandler)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
