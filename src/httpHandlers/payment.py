from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

from django.utils import simplejson

from httpHandlers.all import Payment

class PaymentRESTfulHandler(webapp.RequestHandler):
    
    def get(self, id):
        payments = []
        query = Payment.all()
        for payment in query:
            payments.append(payment.toDict())
        payments = simplejson.dumps(payments)
        self.response.out.write(payments)
    
    def post(self, id):
        payment = simplejson.loads(self.request.body)
        payment = Payment(
            name  = payment['name'],
            value = int(payment['value'])
        )
        payment.put()
        payment = simplejson.dumps(payment.toDict())
        self.response.out.write(payment)

    def put(self, id):
        payment = Payment.get_by_id(int(id))
        tmp = simplejson.loads(self.request.body)
        payment.name  = tmp['name']
        payment.value = int(tmp['value'])
        payment.put()
        payment = simplejson.dumps(payment.toDict())
        self.response.out.write(payment)
        
    def delete(self, id):
        payment = Payment.get_by_id(int(id))
        payment.delete()
            
application = webapp.WSGIApplication([('/api/payment/?([0-9]*)', PaymentRESTfulHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
