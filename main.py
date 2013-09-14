"""
electricalbanana, infobot for IRC
Copyright (C) 2013 Alex Lardner

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import yaml
from twisted.words.protocols import irc
from twisted.python import log
from twisted.internet import reactor, protocol
import time, sys

with open('cfg.yml', 'r') as f:
	config = yaml.load(f)

nick = config["nick"]
port = config["port"]
network = config["network"]
mainc = config["mainchannel"]
logc = config["logchannel"]

mainc = "#" + mainc
logc = "#" + logc
logf = chanlog

class Logger: #he's a lumberjack and he's ok
	def __init__(self, file):
		self.file = logf
		open

	def log(self, message):
		timestamp = time.strftime("[%H:%M:%S", time.localtime(time.time()))
		self.file.write('%s %s\n' % (timestamp, message))
		self.file.flush()

	def close(self):
		self.file.close()

class BananaBot(irc.IRCClient): #The main bot
	nickname = nick

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		self.logger = Logger(open(self.factory.filename, "a"))
		self.logger.log("[connected at %s]" % time.asctime(time.localtime(time.time())))
		#self.logger.close

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		self.logger.log("[disconnected at %s]" % time.asctime(time.localtime(time.time())))
		self.logger.close()

	"""
	event callbacks (a lot of this network and backend stuff is taken from twisted irc's logbot example and altered as I need because it's a good way to learn the library, plus this kind of stuff is pretty standard across the board)
	"""

	def signedOn(self):
		self.join(self.factory.channel)

	def joined(self, channel)
		self.logger.log("[%s joined %s]" % (nick, channel))

	def privmsg(self, user, channel, msg): 
		"""
		This is saying things! this is important and will be _greatly_ expanded upon later.
		"""
		user = user.split('!', 1)[0]
		self.logger.log




class BananaFactory(protocol.ClientFactory): #factory for bots
	def __init__(self, channel):
		self.channel = mainc

	def buildProtocol(self, addr):
		p = BananaBot()
		p.factory = self
		return p

	def clientConnectionLost(self, connector, reason):
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "Connection Failed: ", reason
		reactor.stop()

f = BananaFactory() #create factory protocol/application

reactor.connectTCP(network, port, f)

reactor.run()

