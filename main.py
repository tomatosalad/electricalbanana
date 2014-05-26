#
#	 main.py for electricalbanana IRC Bot
#    Copyright (C) 2013 Alex Lardner
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA

import log
import netcode

class BananaCore:

	def static_responses():
		if re.match('%s[:,] hello' % nick, msgIn, re.IGNORECASE):
			self.pubout(channelIn, "Hello!")
			log.logger.info("Saying hello to %s in %s" % (userIn, channelIn))

		if re.match('botsnack', msgIn, re.IGNORECASE):
			self.pubout(channelIn, ":D")

		if re.match('%s[:,] stats' % nick, msgIn, re.IGNORECASE):
			self.pubout(channelIn, ("I am %s, a bot based on the project %s and I am version %s. "+
			"My creator is tomatosalad and you can bug him at http://tomatosalad.net. You should "+
			"bug him to add more stuff to this, or code it in yourself (ask me for my source).")
			% (nick, projectname, versionnumber))