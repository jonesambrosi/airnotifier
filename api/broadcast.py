#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012, Dongsheng Cai
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Dongsheng Cai nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL DONGSHENG CAI BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from httplib import BAD_REQUEST, LOCKED, FORBIDDEN, NOT_FOUND, \
    INTERNAL_SERVER_ERROR, OK, ACCEPTED
from routes import route
from api import APIBaseHandler
import random
import time
from constants import DEVICE_TYPE_IOS
from pushservices.apns import PayLoad
from pushservices.gcm import GCMException
import logging

@route(r"/api/v2/broadcast/")
class BroadcastHandler(APIBaseHandler):
    def post(self):
        if not self.can('send_broadcast'):
            self.send_response(FORBIDDEN, dict(error="No permission to send broadcast"))
            return
        # if request body is json entity
        data = self.json_decode(self.request.body)
        # the cannel to be boradcasted
        channel = data.get('channel', 'default')
        # iOS and Android shared params
        alert = ''.join(data.get('alert', '').splitlines())
        # iOS
        sound = data.get('sound', None)
        badge = data.get('badge', None)
        self.add_to_log('%s broadcast' % self.appname, alert, "important")
        self.application.send_broadcast(self.appname, self.db, channel, alert)
        delta_t = time.time() - self._time_start
        logging.info("Broadcast took time: %sms" % (delta_t * 1000))
        self.send_response(ACCEPTED)
