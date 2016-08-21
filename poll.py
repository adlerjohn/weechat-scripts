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
SCRIPT_VERSION = '0.0.1'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Polls messages and automatically downloads new files that match criteria.'
SCRIPT_SHUTDOWN = ''
SCRIPT_CHARSET = 'UTF-8'

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
# Main
#---------------
def main():
	weechat.prnt('', 'Hello world!')

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

