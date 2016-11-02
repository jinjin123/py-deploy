from tornado.web import RequestHandler

class NotFoundHandler( RequestHandler ) :
    """ for not found error """
    def get(self, *args, **kwargs):
        self.redirect('/')

