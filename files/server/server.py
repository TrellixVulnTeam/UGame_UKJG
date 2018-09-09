from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse as urlparse
import json
import os
import time

class S(BaseHTTPRequestHandler):
	def _set_headers(self, res=200, type="text/html", loc=False):
		self.send_response(res)
		if loc:
			self.send_header('Location', loc)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		if self.client_address[0]=="127.0.0.1":
			self.do_POST();
		else:
			self._set_headers(200)
			self.wfile.write(b"<tt><h1>UGame-Server.</h1></tt><hr>Incorrect Method.")

	def do_HEAD(self):
		self._set_headers()
		
	def do_POST(self):
		if self.headers.get('Content-Length'):
			data = json.loads(self.rfile.read(int(self.headers.get('Content-Length'))));
		else:
			data = {};
		datas = json.dumps(data);
		if self.path == "/":
			self._set_headers(200, "text/html", "index");
			self.path = "/index";
		else:
			self._set_headers(200, "text/html");
		path = self.path[1:];
		print(path);
		import index as serverfile;
		auth=True;
		if path[:6]=="secure":
			auth=False;
			os.chdir("axs");
			if "hash" in data:
				if os.path.exists(data["hash"]+".txt") and time.time()-os.path.getmtime(data["hash"]+".txt")<43200:
					auth=True;
					print("Secure access from account "+data["name"]+" verified.");
			os.chdir("..");
		if auth:
			try:
				exec("global response; response = serverfile."+path+"(data);");
			except AttributeError:	
				exec('global response; response = "Method not found.";');
		else:
			exec('global response; response = "Authentification Failed.";');
		print("Sending response: "+response);
		self.wfile.write(bytes(response, 'utf8'));
		
			
def run(server_class=HTTPServer, handler_class=S, port=1103):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('Starting httpd...');
	httpd.serve_forever()

if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()