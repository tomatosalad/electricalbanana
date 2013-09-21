electricalbanana
================

An infobot in Python by [tomatosalad](http://tomatosalad.net)

electricalbanana is licensed under GPLv3, except for log.py from pyGBot which is GPLv2.

The basic netcode is derived from pyGBot's.

Features
--------

*While this section is currently small, many are planned and being worked on!*

* Custom URI schemes: `github://` will link to a user (and repo, if desired)
					  `wiki://` will link to [Wikipedia](http://en.wikipedia.org). Use underscores as spaces.
					  `google://` will link to a pre-filled Google Search box. Use plus signs as spaces.
					  `trope://` will link to [TVTropes](http://tvtropes.org). Just CamelCase it.
					  `xkcd://` followed by a number will link to that [xkcd](http://xkcd.com). Randall provides JSON
					  transcripts of the comics, so the ability to search comics is a totally doable
					  feature.
					  `qc://` will similarly link to that [Questionable Content](http://questionablecontent.net) comic.
					  `ksp://` will link to the Kerbal Space Program wiki. Use underscores as spaces.

* Coin flipping: `/me flips a coin` will give you either heads or tails.

How To
------

You will need Twisted and PyYAML.

Edit cfg.yml. The only field that you can leave empty is `serverpassword`. SSL is untested, leave it as "false" unless
you are willing to test it.

Run `python run.py` at a shell prompt and enter your NickServ password when prompted. You need a registered nickname
and password for electricalbanana to work properly. 

It is recommended that you run electricalbanana in a GNU Screen. Kill it with a simple `^C` (a more elegant solution is being
devised for the future).

Known Issues
------------
* Logging is horribly broken.

Planned Features
----------------
* Four-function calculator
* Moderator bot capabilities
* Configuration options for certain bot functions
* Google Translate
* The ability to recognize channel operators and perform op-only commands
* Weather by US zipcodes
* Web page title retriever
* 8-ball responses
* Message electricalbanana to retrieve a scrollback from a channel (up to 50 lines)
* Move all bot functions to a seperate file
