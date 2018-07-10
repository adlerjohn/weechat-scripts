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
SCRIPT_VERSION = '0.1.6'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'Polls messages and automatically downloads new files that match criteria.'
SCRIPT_SHUTDOWN = ''
SCRIPT_CHARSET = 'UTF-8'

SCRIPT_OPTIONS = {
    'files' : '',
    'hosts' : '',
    'nicks' : '',
}

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
    l = s.lower()
    for word in words.lower().split():
        if word not in l:
            return False
    return True

def parse_tags(tags, tag):
    pattern = re.compile(r'^' + tag + '_(.*)$', re.IGNORECASE)
    for t in tags:
        match = pattern.match(t)
        if not match:
            continue
        return match.group(1)
    return None

#---------------
# Handlers
#---------------
def config_cb(data, option, value):
    weechat.config_set_plugin(option, value)
    return weechat.WEECHAT_RC_OK

def message_cb(
    data,
    buf,
    date,
    tags,
    displayed,
    highlight,
    prefix,
    message
):
    files = weechat.config_get_plugin('files').split(',')
    hosts = weechat.config_get_plugin('hosts').split(',')
    nicks = weechat.config_get_plugin('nicks').split(',')

    tags = list(tags.split(','))

    # Ignore join/leave message
    if 'irc_smart' in tags or 'irc_smart_filter' in tags:
        return weechat.WEECHAT_RC_OK

    # Extract the host
    host = parse_tags(tags, 'host')
    if not host:
        return weechat.WEECHAT_RC_OK

    # Extract the nick
    nick = parse_tags(tags, 'nick')
    if not nick:
        return weechat.WEECHAT_RC_OK

    # Check if the current host or nick matches our list of accpeted hosts or nicks
    if host not in hosts and nick not in nicks:
        return weechat.WEECHAT_RC_OK

    weechat.log_print(' caught message: ' + str(message));

    # Compare the message against list of files
    do_download = False
    for f in files:
        if words_in_string(f, message):
            do_download = True
            break
    if not do_download:
        return weechat.WEECHAT_RC_OK

    # If a match, extract download prompt from message
    match = re.match(r'^.*([/]msg.*)$', message, re.IGNORECASE)
    if not match:
        return weechat.WEECHAT_RC_OK
    msg = match.group(1)

    # Download file
    weechat.command(buf, msg)

    return weechat.WEECHAT_RC_OK

#---------------
# Main
#---------------
def main():
    weechat.log_print(' Running ' + str(SCRIPT_NAME) + ' version ' + str(SCRIPT_VERSION));

    # Read options
    for option, default_value in SCRIPT_OPTIONS.items():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default_value)

    files = weechat.config_get_plugin('files').split(',')
    hosts = weechat.config_get_plugin('hosts').split(',')
    nicks = weechat.config_get_plugin('nicks').split(',')
    weechat.log_print(' files = ' + str(files));
    weechat.log_print(' hosts = ' + str(hosts));
    weechat.log_print(' nicks = ' + str(nicks));

    # Callback to update options
    weechat.hook_config('plugins.var.python.' + SCRIPT_NAME + '.*', 'config_cb', '')

    # Callback to process messages
    weechat.hook_print('', '', '', 1, 'message_cb', '')

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

