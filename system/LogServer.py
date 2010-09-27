#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programming contest management system
# Copyright (C) 2010 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright (C) 2010 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright (C) 2010 Matteo Boscariol <boscarim@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from SimpleXMLRPCServer import SimpleXMLRPCServer
import Configuration
import datetime
import time
import os
from Utils import Logger, format_log, maybe_mkdir

class LogServer:
    def __init__(self, listen_address = None, listen_port = None):
        if listen_address == None:
            listen_address = Configuration.log_server[0]
        if listen_port == None:
            listen_port = Configuration.log_server[1]

        # Create server
        server = SimpleXMLRPCServer((listen_address, listen_port), logRequests = False)
        server.register_introspection_functions()

        server.register_function(self.log)

        maybe_mkdir("logs")
        self.log_file = open(os.path.join("logs", "%d.log" % (time.time())), "w")

        # Run the server's main loop
        server.serve_forever()

    def log(self, msg, service, severity = Logger.SEVERITY_NORMAL, timestamp = None):
        if timestamp == None:
            timestamp = time.time()
        line = format_log(msg, service, severity, timestamp)
        print line
        print >> self.log_file, line
        return True

if __name__ == "__main__":
    ls = LogServer()
