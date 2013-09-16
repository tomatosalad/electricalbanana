"""
electricalbanana, infobot for IRC
Copyright (C) 2013 Alex Lardner

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
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

import log

with open('cfg.yml', 'r') as f:
	config = yaml.load(f)

nick = config["nick"]
port = config["port"]
network = config["network"]
mainc = config["mainchannel"]
logc = config["logchannel"]
fname = config["fullname"]
uname = config["username"]
passwd = config["serverpassword"]
nsname = config["nickservname"]
logfile = config["logfile"]
chatfile = config["chatlogfile"]
sslpref = config["ssl"]

#if fname == None:
#	fname = "Mellow Yellow"

versionname = "Electrical Banana"
versionnumber = "0.1.0"


"""Add these back in if you don't want to use quotes in cfg.yml
mainc = "#" + mainc 
logc = "#" + logc

"""

#basically all the netcode is derived/copied from pygbot's, specifically https://github.com/pyGBot/pyGBot/blob/master/pyGBot/core.py

class BananaBot(irc.IRCClient):

	def pubout(self, channel, msg):
		msgOut = unicodeOut(msg)
		channelOut = unicodeOut(channel)
		self.say(channel=channelOut, message=msgOut)

		#strip color codes
		log.chatlog.info('[PUB->%s]%s') % (channelOut, stripcolors(msgOut))

	def privout(self, user, msg):
		msgOut = unicodeOut(msg)
		userOut = unicodeOut(msg)
		self.msg(user=userOut, message=msgOut)

		log.chatlog.info('[PRV->%s]%s' % (userOut, stripcolors(msgOut)))

	def replyout(self, channel, user, msg):
		msgOut = unicodeOut(msg)
		userOut = unicodeOut(msg)
		channelOut = unicodeOut(channel)
		if (channel is None):
			self.privout(userOut, msgOut)
		else:
			self.pubout(channelOut, msgOut)

	def noteout(self, user, msg):
		msgOut = unicodeOut(msg)
		userOut = unicodeOut(msg)
		self.notice(user=userOut, message=msgOut)

		log.chatlog.info('[NOTICE->%s]%s' % (channelOut, stripcolors(msgOut)))

	def invite(self, user, channel):
		userOut=unicodeOut(user)
		channelOut=unicodeOut(channel)
		self.sendLine("INVITE %s %s" % (userOut, channelOut))

		log.chatlog.info('[INVITE->%s] %s' % (userOut, channelOut))

	def joinChannel(self, channel, key=None):
		channelOut = unicodeOut(channel)
		if key:
			keyOut = unicodeOut(key)
			self.join(channel=channelOut, key=keyOut)
		else:
			self.join(channel=channelOut)

	def actout(self, channel, msg):
		msgOut = unicodeOut(msg)
		channelOut = unicodeOut(channel)
		self.me(channel=channelOut, action=msgOut)

		log.chatlog.info('[ACT->%s]%s' % (channelOut, stripcolors(msgOut)))

	def modestring(self, target, modestring):
		self.sendLine("MODE %s %s" % (target, modestring))

		log.chatlog.info('[MODE] %s %s' % (target, modestring))

	def __init__(self):

		npasswd = raw_input("Please enter your NickServ password: ")

		self.nickname = nick
		self.idpass = npasswd
		self.idnick = nsname

		self.realname = fname
		self.usermodes = "+iwB"

		#insert op password stuff here if desired
		
		if passwd:
			self.password = passwd

		self.lineRate = float(2)

		self.versionName = versionname
		self.versionNumber = versionnumber

		self.whois = []

		self.channelusers = {}
		self.channels = []

		self.versionEnv = sys.platform

	#connection callbacks

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)
		log.logger.info("[Connected at %s]" % time.asctime(time.localtime(time.time())))

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)
		log.logger.info("[Disconnected at %s:%s" % (time.asctime(time.localtime(time.time())), reason))

	#event callbacks

	def signedOn(self):

		self.regNickServ()

		self.modestring(self.nickname, self.usermodes)

		for channel in self.factory.channel:
			self.joinChannel(channel)

	def regNickServ(self):
		if hasattr(self, 'idnick') and hasattr(self, 'idpass'):
			self.privout('%s' % (self.idnick,), 'identify %s' % (self.idpass,))

	def joined(self, channel): 			#this stuff gets called when joining a channel
		log.logger.info('[I have joined %s]' % (channel,))
		self.channels.append(channel)

		channelIn = unicodeIn(channel)

	def left(self, channel):
		if channel in self.channels:
			self.channels.remove(channel)

	def kickedFrom(self, channel, kicker, message):
		if channel in self.channels:
			self.channels.remove(channel)

		channelIn = unicodeIn(channel)
		kickerIn = unicodeIn(kicker)
		messageIn = unicodeIn(message)

	def noticed(self, user, channel, msg):		#called on notices
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		channelIn = unicodeIn(channel)
		msgIn = unicodeIn(msg)
		log.chatlog.info('[NOTICE<-]<%s> %s' % (user, msg))

	def privmsg(self, user, channel, msg):		#called upon recieving message
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		channelIn = unicodeIn(channel)
		msgIn = unicodeIn(msg)

		if channel.upper() == self.nickname.upper():
			if msgIn.startswith('auth'):
				msgNoPwd = msgIn.split(' ')
				if len(msgNoPwd) > 2:
					msgNoPwd[2] = '*' * 8
				msgNoPwd = ' '.join(msgNoPwd)
				log.chatlog.info('[PRV<-]<%s> <%s>' % (user, msgNoPwd))
			else:
				log.chatlog.info('[PRV<-]<%s> <%s>' % (userIn, msgIn))
		else:
			log.chatlog.info('[PUB<-]<%s> %s' % (user, msg))

	def action(self, user, channel, message):
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		channelIn = unicodeIn(channel)
		msgIn = unicodeIn(msg)
		log.chatlog.info('* %s %s' % (user, msg))

	def topicUpdated(self, user, channel, newTopic):
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		channelIn = unicodeIn(channel)
		newTopicIn = unicodeIn(newTopic)
		log.chatlog.info('Topic for %s set by %s: %s' % (channel, user, newTopic))

	def userJoined(self, user, channel):
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		channelIn = unicodeIn(channel)
		log.chatlog.info('%s joined %s' % (user, channel))

	def userLeft(self, user, channel):
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		channelIn = unicodeIn(channel)
		log.chatlog.info('%s left %s' % (user, channel))

	def userKicked(self, user, channel, kicker, message):
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		channelIn = unicodeIn(channel)
		kickerIn = unicodeIn(kicker)
		messageIn = unicodeIn(message)

		log.chatlog.info('%s was kicked from %s by %s: %s' % (user, channel, kicker, message))

	def userQuit(self, user, quitMessage):
		user = user.split('!', 1)[0]
		userIn = unicodeIn(user)
		quitMsgIn = unicodeIn(quitMessage)

		log.chatlog.info('%s has quit [%s]' % (user, quitMessage))

	def userRenamed(self, oldname, newname):
		oldnameIn = unicodeIn(oldname)
		newnameIn = unicodeIn(newname)
		log.chatlog.info('%s is now known as %s' % (oldname, newname))

	def cprivmsg(self, channel, user, message):
		msgOut = unicodeOut(msg)
		userOut = unicodeOut(user)
		channelOut = unicodeOut(channel)
		fmt = "CPRIVMSG %s %s: %%s" % (userOut, channelOut)
		self.sendLine(fmt % (message,))

	def cnotice(self, channel, user, message):
		msgOut = unicodeOut(msg)
		userOut	= unicodeOut(user)
		channelOut = unicodeOut(channel)
		fmt = "CNOTICE %s %s:%%s" % (userOut, channelOut)
		self.sendLine(fmt % (messageOut,))

class BananaBotFactory(protocol.ClientFactory):
	"""Factory for bots.

	A new protocol instance will be created every time we connect.
	"""

	protocol = BananaBot

	def __init__(self, channel, filename):
		self.channel = channel
		self.filename = filename

		#console log stuff
		try:
			print "Opening Log File..."
			log.addScreenHandler(log.logger, log.formatter)
			log.addLogFileHandler(log.logger,logfile,log.formatter)
		except IOError, msg:
			print "Unable to open log file: ", msg
			print "Defaulting to local."
			log.addLogFileHandler(log.logger,'bananabot,log',log.formatter)
		except KeyError:
			print "No log file config found, using default."		
			log.addLogFileHandler(log.logger,'bananabot.log',log.formatter)							

		#chatlog stuff
		try:
			print "Opening Log File..."
			log.addLogFileHandler(log.chatlog,chatfile,log.cformat)
		except IOError, msg:
			print "Unable to open log file: ", msg
			print "Defaulting to local."
			log.addLogFileHandler(log.chatlog,'bananachat.log',log.cformat)
		except KeyError:
			print "No log file config found, using default."
			log.addLogFileHandler(log.chatlog,'bananachat.log',log.cformat)

	def clientConnectionLost(self, connector, reason):
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		log.logger.critical('connection failed: %s', (str(reason),))
		reactor.stop()

def stripcolors(inmsg):	
	inmsg = inmsg.replace("\x02\x0301,00", '')
	inmsg = inmsg.replace("\x02\x0302,00", '')
	inmsg = inmsg.replace("\x02\x0303,00", '')
	inmsg = inmsg.replace("\x02\x0304,00", '')
	inmsg = inmsg.replace("\x0F", '')
	return inmsg

def unicodeOut(msg):
	if isinstance(msg, unicode):
		encMsg = msg.encode('utf-8', 'replace')
	else:
		encMsg = msg
	return encMsg

def unicodeIn(msg):
	if isinstance(msg, unicode):
		decMsg = msg
	else:
		decMsg = msg.encode('utf-8', 'replace')
	return decMsg

def run():
	channel = mainc.split()
	host = network

	localport = None #these aren't needed at all but I'm keeping them for the future
	localaddr = None

	sslconnect = False
	if sslpref == "true":
		sslconnect = True
		from twisted.internet import ssl

	print "Initialising Factory..."
	fact = BananaBotFactory(channel, 'UNUSED')
	if sslconnect:
		cfact = ssl.ClientContextFactory()

	print "Connecting..."

	try:
		if sslconnect:
			reactor.connectSSL(host, port, fact, cfact)
		else:
			reactor.connectTCP(host, port, fact)

		reactor.run()
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise