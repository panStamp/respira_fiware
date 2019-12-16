#########################################################################
# Copyright (c) 2019 panStamp <contact@panstamp.com>
# 
# This file is part of the RESPIRA-FIWARE project.
# 
# panStamp  is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
# 
# panStamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with panStamp; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 
# USA
#
# Author: Daniel Berenguer
# Date: Dec 13 2019
#########################################################################

from config.config import FcbgConfig
from fcbgexception import FcbgException
from fcbghttpclient import FcbgHttpClient

import threading
import cherrypy
from cherrypy.lib import auth_basic
import json
import os


class FcbgHttpServer(threading.Thread):
    """
    HTTP server
    """

    @cherrypy.expose
    def notify(self):
        """
        HTTP call to /notify
        """
        if cherrypy.request.process_request_body:
            try:
                body = cherrypy.request.body.read()        
                notification = json.loads(body)
                self.manager.notify(notification)
            except:
                cherrypy.response.status = 400
                return "Unable to handle request"

        cherrypy.response.status = 200
        return "OK"


    def stop(self):
        """
        Stop HTTP server
        """        
        cherrypy.engine.exit()    


    def run(self):
        """
        Start web server
        """       
        conffile = os.path.join(os.path.dirname(__file__), "config", "webserver.conf")
        cherrypy.config.update(conffile)
        www_dir = os.path.join(os.path.dirname(__file__), "www")

        confdict = {"global" : {
                            "server.socket_port": FcbgConfig.HTTP_SERVER_PORT},
                    "/www" : {
                           "tools.staticdir.root" : www_dir}
                    }

        cherrypy.config.update(confdict)
        
        app = cherrypy.tree.mount(self, '/', conffile)
        app.merge(confdict)
        
        if hasattr(cherrypy.engine, "signal_handler"):
            cherrypy.engine.signal_handler.subscribe()
        if hasattr(cherrypy.engine, "console_control_handler"):
            cherrypy.engine.console_control_handler.subscribe()
        cherrypy.engine.start()
        cherrypy.engine.block()


    def __init__(self, manager):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)

        ## Parent manager process
        self.manager = manager
