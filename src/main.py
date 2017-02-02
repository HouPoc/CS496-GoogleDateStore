from google.appengine.ext import ndb
from ndb_definition import *
import json
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
    
    def delete(self):
        ndb.delete_multi(Books.query().fetch(keys_only=True))    
        ndb.delete_multi(Customers.query().fetch(keys_only=True))

class BookHandler(webapp2.RequestHandler):		#Handlers for actions related to book
    def put(self):					#Hnadlers for post requests
        book_data = json.loads(self.request.body)	#load the data
        new_book = Books(
            title = book_data['title'],
            isbn = book_data['isbn'],
            genre = book_data['genre'],
            author = book_data['author'],
            check_in = book_data['checkedIn']
        )
        new_book.put()
        book_dict = new_book.to_dict()
        book_dict['id'] = new_book.key.id()
        self.response.write(json.dumps(book_dict))

    def get(self, **args):   			        #Get Request Handler
        if 'book_id' in args:
            query_book = ndb.Key(Books, int(args['book_id']))
       	    back_data = query_book.get()
            return_data = back_data.to_dict()
            return_data['id'] = back_data.key.id()
            self.response.write(json.dumps(return_data)) 
        else:
            query_key = self.request.get('check_in')
            if query_key:
                checkedIn = (query_key == "true")
                query_book = Books.query(Books.check_in == checkedIn)
                book_list = query_book.fetch()
                back_data = []
                for item in book_list:
                    single_book = item.to_dict()
                    single_book['id'] = item.key.id()
                    back_data.append(single_book)
                self.response.write(json.dumps(back_data))
            else:				
                query_book = Books.query()
                book_list = query_book.fetch()
                back_data = []
                for item in book_list:
                    single_book = item.to_dict()
                    single_book['id'] = item.key.id()
                    back_data.append(single_book)
                self.response.write(json.dumps(back_data))  

    def delete(self, **args):
        query_book = ndb.Key(Books, int(args['book_id']))
        target_book = query_book.get()
        target_book_id = target_book.key.id()
        target_book.key.delete()
        self.response.write("book %d has been deleted" % target_book_id)
        
    def patch(self, **args):
        query_book = ndb.Key(Books, int(args['book_id']))
        target_book = query_book.get()
        update_data = json.loads(self.request.body)
        if 'title'in update_data:
            target_book.title = update_data['title']
        if 'isbn' in update_data:
            target_book.isbn = update_data['isbn']
        if 'author' in update_data:
            target_book.author = update_data['author']
        if 'genre' in update_data:
            target_book.genre = update_data['genre']
        if 'check_in' in update_data:
            target_book.check_in = update_data['check_in']
        target_book.put()
        back_data = target_book.to_dict()
        back_data['id'] = target_book.key.id() 
        self.response.write(json.dumps(back_data))
 
class CustomerHandler(webapp2.RequestHandler):
    def put(self):
        customer_data = json.loads(self.request.body)
        new_customer = Customers(
            name = customer_data['name'],
            balance = float(customer_data['balance']),
            check_out = customer_data['checked_out']
        )
        new_customer.put()
        customer_dict = new_customer.to_dict()
        customer_dict['id'] = new_customer.key.id()
        self.response.write(json.dumps(customer_dict))

    def get(self, **args):
        if 'customer_id' in args:
            query_customer = ndb.Key(Customers, int(args['customer_id']))
            back_data = query_customer.get()
            return_data = back_data.to_dict()
            return_data['id'] = back_data.key.id()
            self.response.write(json.dumps(return_data))   
        else:
            query_customer = Customers.query()
            customer_list = query_customer.fetch()
            back_data = []
            for item in customer_list:
                single_customer = item.to_dict()
                single_customer['id'] = item.key.id()
                back_data.append(single_customer)
            self.response.write(json.dumps(back_data))

    def delete(self, **args):
        query_customer = ndb.Key(Customers, int(args['customer_id']))
        target_customer = query_customer.get()
        target_customer_id = target_customer.key.id()
        target_customer.key.delete()
        self.response.write("customer %d has been deleted" % target_customer_id)
 
    def patch(self, **args): 
        query_customer = ndb.Key(Customers, int(args['customer_id']))
        target_customer = query_customer.get()
        update_data = json.loads(self.request.body)
        if 'name'in update_data:
           target_customer.name = update_data['name']
        if 'balance' in update_data:
           target_customer.balance = update_data['balance']
        if 'check_out' in update_data:
           target_customer.check_out = update_data['check_out']
        target_customer.put()
        back_data = target_customer.to_dict()
        back_data['id'] = target_customer.key.id() 
        self.response.write(json.dumps(back_data))

class EventHandler(webapp2.RequestHandler):
    def put(self, **args):
        if ('customer_id' in args and 'book_id' in args):
            query_customer = ndb.Key(Customers, int(args['customer_id']))
            query_book = ndb.Key(Books, int(args['book_id']))
            book = query_book.get()
            book.check_in = False
            book.put()
            customer = query_customer.get()
            book_link = ("/books/%d" % book.key.id())
            customer.check_out.append(book_link)
            customer.put()
            return_book = ndb.Key(Customers, int(args['customer_id'])).get()
            return_data = return_book.to_dict()
            return_data['id'] = return_book.key.id()
            self.response.write(json.dumps(return_data))

    def get(self, **args):
        if ('customer_id' in args and 'book_id' in args):
            query_customer = ndb.Key(Customers, int(args['customer_id']))
            query_book = ndb.Key(Books, int(args['book_id']))
            customer = query_customer.get()
            book = query_book.get()
            book_link = ("/books/%d" % book.key.id())
            if book_link in customer.check_out:
                return_data = book.to_dict()
                return_data['id'] = book.key.id()
                self.response.write(json.dumps(return_data))
            else:
                self.response.write("this book is not checked out")
         else if 'customer_id' in args:
            query_customer = ndb.Key(Customers, int(args['customer_id']))
            customer = query_customer.get()
            book_id = []
            from item in query_customer.check_out:
                book_id.append(int(item[7:]))
            self.response.write(json.dumps(book_id))


    def delete(self, **args):
        if ('customer_id' in args and 'book_id' in args):
            query_customer = ndb.Key(Customers, int(args['customer_id']))
            query_book = ndb.Key(Books, int(args['book_id']))
            book = query_book.get()
            book.check_in = True
            book.put()
            customer = query_customer.get()
            book_link = ("/books/%d" % book.key.id())
            customer.check_out.remove(book_link)
            customer.put()
            return_book = ndb.Key(Customers, int(args['customer_id'])).get()
            return_data = return_book.to_dict()
            return_data['id'] = return_book.key.id()
            self.response.write(json.dumps(return_data))


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/books', BookHandler),
    ('/customers', CustomerHandler)
], debug=True)
app.router.add(webapp2.Route('/books/<book_id:\d+>', handler=BookHandler))
app.router.add(webapp2.Route('/customers/<customer_id:\d+>', handler=CustomerHandler))
app.router.add(webapp2.Route('/customers/<customer_id:\d+>/books/<book_id:\d+>', handler=EventHandler))
