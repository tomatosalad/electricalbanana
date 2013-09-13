import yaml
from twisted.words.protocols import irc
from twisted.python import log
from twisted.internet import reactor, protocol
import time

with open('cfg.yml', 'r') as f:
	config = yaml.load(f)

nick = config["nick"]
port = config["port"]
network = config["network"]
mainc = config["mainchannel"]
logc = config["logchannel"]

class BananaFactory(protocol.ClientFactory): #factory for bots
	def __init__(self, channel):
		self.channel = mainc

	def buildProtocol(self, addr):
		p = BananaBot()
		p.factory = self
		return p

	def clientConnectionLost(self, connector, reason):
		#connector.conne

	def clientConnectionFailed(self, connector, reason):
		print "Connection Failed: ", reason
		reactor.stop()