# poll.py
# Copyright (C) 2016  John Adler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

SCRIPT_NAME = 'poll'
SCRIPT_AUTHOR = 'John Adler'
SCRIPT_VERSION = '0.1.0'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Polls messages and automatically downloads new files that match criteria.'
SCRIPT_SHUTDOWN = ''
SCRIPT_CHARSET = 'UTF-8'

FILES = [
	]
HOSTS = [
	]

#---------------
# Imports
#---------------
try:
	import weechat
	import os
	import re
	IMPORT_OK = True
except ImportError as error:
	IMPORT_OK = False
	if str(error).find('weechat') != -1:
		print('This script must be run from WeeChat.')
	else:
		weechat.prnt('', 'poll: {0}'.format(error))

#---------------
# Utility
#---------------
def words_in_string(words, s):
	return set(words.split()).intersection(s.split())

#---------------
# Handlers
#---------------
def handle_message(
	data,
	buf,
	date,
	tags,
	displayed,
	highlight,
	prefix,
	message
):
	tags = list(tags.split(','))

	# Ignore join/leave message
	if 'irc_smart' in tags or 'irc_smart_filter' in tags:
		return weechat.WEECHAT_RC_OK

	# Check if the 'host_' substring is in the tags
	host_str = [s for s in tags if 'host_' in s]
	if len(host_str) != 1:
		return weechat.WEECHAT_RC_OK
	host_str = host_str[0]

	# Extract the host
	host = host_str.split("_", 1)
	if len(host) != 2:
		return weechat.WEECHAT_RC_OK
	host = host[1]

	# Check if the current host matches our list of hosts
	if host not in HOSTS:
		return weechat.WEECHAT_RC_OK

	# Compare the message against list of files
	do_download = False
	for f in FILES:
		if words_in_string(f, message):
			do_download = True
			break
	if not do_download:
		return weechat.WEECHAT_RC_OK

	# If a match, extract download prompt from message
	match = re.match(r'^.*([/][mM][sS][gG].*)$', message)
	if not match:
		return weechat.WEECHAT_RC_OK
	msg = match.group(1)

	# Download file
	weechat.command("", msg)

	return weechat.WEECHAT_RC_OK

#---------------
# Main
#---------------
def main():
	weechat.hook_print('', '', '', 1, 'handle_message', '')

if __name__ == '__main__' and IMPORT_OK and weechat.register(
	SCRIPT_NAME,
	SCRIPT_AUTHOR,
	SCRIPT_VERSION,
	SCRIPT_LICENSE,
	SCRIPT_DESC,
	SCRIPT_SHUTDOWN,
	SCRIPT_CHARSET
):
	main()

