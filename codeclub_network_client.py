import sys
import Pyro4
import threading

class CodeClubNetworkClient:
	def __init__(self):
		sys.excepthook=Pyro4.util.excepthook
		self.daemon = Pyro4.Daemon(host=Pyro4.socketutil.getInterfaceAddress("www.google.com"))
		t = threading.Thread(target=lambda: self.daemon.requestLoop())
		t.daemon = True
		t.start()

	def connect_to_object_on_network(self, name):
		return Pyro4.Proxy("PYRONAME:"+name)

	def make_local_object_available_on_network(self, local_object):
		return self.daemon.register(local_object)
