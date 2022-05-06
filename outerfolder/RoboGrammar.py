from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.parse import unquote
import json
import threading
from RobotInterpreter import RobotInterpreter




class RoboGrammerServer(BaseHTTPRequestHandler):



	def __call__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def __init__(self, interpreter):
		self.interpreter = interpreter
	
	def do_GET(self):

		urlParsed = urlparse(self.path)
		data = parse_qs(urlParsed.query)["data"][0]

		asJson = json.loads(unquote(data))
		succeed, result = self.interpreter.handleCommand(asJson)

		if succeed == True:
			self.send_response(200, 'OK')
		else:
			self.send_response(418)

		result = str(result)

		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Content-type', 'html')
		self.end_headers()

		# self.wfile.write(bytes(result, "utf-8"))



class RoboGrammar:


	hostName = "localhost"
	serverPort = 1234
	


	def __init__(self,robot,srAgent,vAgent):
		self.robotInterperter = RobotInterpreter(robot,srAgent,vAgent)
		self.thread = threading.Thread(target=self.run)
		self.thread.start()


	def run(self):

		handler = RoboGrammerServer(self.robotInterperter)

		webServer = HTTPServer((self.hostName, self.serverPort), handler)
		print("Server started http://%s:%s" % (self.hostName, self.serverPort))

		try:
			webServer.serve_forever()
		except KeyboardInterrupt:
			pass

		webServer.server_close()
		print("Server stopped.")



if __name__ == "__main__":
	RoboGrammar(None)
