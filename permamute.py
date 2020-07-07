# ################################################################### #
#                                                                     #
#  BigBrotherBot(B3) (www.bigbrotherbot.net)                          #
#  Copyright (C) 2005 Michael "ThorN" Thornton                        #
#                                                                     #
#  This program is free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License        #
#  as published by the Free Software Foundation; either version 2     #
#  of the License, or (at your option) any later version.             #
#                                                                     #
#  This program is distributed in the hope that it will be useful,    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the       #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with this program; if not, write to the Free Software        #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA      #
#  02110-1301, USA.                                                   #
#                                                                     #
# ################################################################### #
__author__ = 'donna30' 
__version__ = '1.0'

import b3
import re
import b3.events
import b3.plugin

class PermamutePlugin(b3.plugin.Plugin):
    requiresConfigFile = False

    #Getting Plugin admin (cannot register commands without it)
    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return

        # Registering events
        self.registerEvent(self.console.getEventID('EVT_CLIENT_JOIN'), self.onJoin)
        # Registering commands
        self._adminPlugin.registerCommand(self, 'permamute', 20, self.cmd_pbmute, 'pbmute')
        self._adminPlugin.registerCommand(self, 'permaunmute', 20, self.cmd_rmpbmute, 'pbunmute')

    def onJoin(self, event):
        client = event.client
        self.check_mute(client)

    def check_mute(self, client):
        if client.bot:
            self.debug('Bot')
        else:
            cursor = self.console.storage.query('SELECT * FROM pbmute WHERE iduser = %s' % client.id)
            sname = str(cursor.getValue('sname'))
            cursor.close()
            if sname == 'None':
                return
            else:
                self.console.write("mute %s 9999999999999" % client.cid)
                client.message('^3You are ^1PERMANENTLY MUTED')
                client.message('^3Request an ^2un-mute ^3via ^5discord!')
                self.console.say("%s ^3is ^1permanently muted" % client.exactName)

    def cmd_pbmute(self, data, client, cmd=None):
        handler = self._adminPlugin.parseUserCmd(data)
        sclient = self._adminPlugin.findClientPrompt(handler[0], client)
        if not data:
            client.message('!pbmute <client>')
            return
        cursor = self.console.storage.query('SELECT * FROM pbmute WHERE iduser = %s' % client.id)
        if cursor.rowcount == 0:
            handler = self._adminPlugin.parseUserCmd(data)
            sname = str(handler[0])
            self.console.write("mute %s" % sclient.cid)
            sclient.message('^3You were ^1PERMANENTLY MUTED ^3by an ^2Admin')
            sclient.message('^3Request an ^2un-mute ^3via ^5discord!')
            self.console.say("%s ^3has been ^1permanently muted ^3by the ^2admin" % sclient.exactName)
            cursor = self.console.storage.query('INSERT INTO pbmute (iduser, sname) VALUES (%i, \'%s\')' % (sclient.id, sname))
            cursor.close()
        else:
            client.message('Client already muted')

    def cmd_rmpbmute(self, data, client, cmd=None):
        handler = self._adminPlugin.parseUserCmd(data)
        sclient = self._adminPlugin.findClientPrompt(handler[0], client)
        if not sclient:
            return
        self.console.storage.query('DELETE FROM pbmute WHERE iduser = %s' % sclient.id)
        self.console.write("mute %s" % sclient.cid)
        client.message('^2unmuted ^5%s' % sclient.name)
        sclient.message('^3You were ^2unmuted ^3by an ^5Admin')
