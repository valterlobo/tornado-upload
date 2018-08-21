import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string 
from tornado.options import define, options
import uuid
define("port", default=8888, help="run on the given port", type=int)

__UPLOADS__ = "uploads/"

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/upload", UploadHandler)
        ]
        tornado.web.Application.__init__(self, handlers)
        
class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("upload_form.html")
        
class UploadHandler(tornado.web.RequestHandler):
    async def post(self):
        fileinfo = self.request.files['file1'][0]
        #print ("fileinfo is %s", fileinfo)
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'wb')
        fh.write(fileinfo['body'])
        self.finish(cname + " is uploaded!! Check %s folder" %__UPLOADS__)

        
def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
