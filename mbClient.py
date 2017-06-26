# -*- coding: utf-8 -*-

"""The most basic chat protocol possible.

sudo kill -TERM $(sudo cat mbClient.pid)
sudo twistd  --python=mbClient.py --pidfile=mbClient.pid --logfile=logs/mbClient.log

"""
port = 14230
delayBeforeDropConnection = 180
getPowerCRC = "\x10\x03\x01\x00\x00\x02\xC6\xB6"


#from twisted.protocols import basic
from twisted.internet import protocol, reactor, error
from twisted.application import service, internet
from twisted.python import log

from struct import pack, unpack
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def get_data_from_mc():
    str2return = pack(">BBBHHBB", 16, 3, 4 , mc.get("CO2"), mc.get("T"), 255, 255)
    return str2return


class MyChat(protocol.Protocol):
    def connectionMade(self):
        log.msg( "Got new client: {}".format(self.transport.getPeer()) )
        self.factory.clients.append(self)
        self.timeout = reactor.callLater(delayBeforeDropConnection, self.dropConnection)

    def connectionLost(self, reason):
        log.msg( "Lost a client! reason: {}".format(reason) )
        self.factory.clients.remove(self)

    def dataReceived(self, line):
        log.msg( "received {}".format( repr(line) ) )
        self.timeout.reset(delayBeforeDropConnection)
        if line==getPowerCRC:
            self.message(get_data_from_mc())

        else:
            log.msg( "Drop connection from server due to unknown client{}".format(self.transport.getPeer()) )
            self.dropConnection()

        # for c in self.factory.clients:
        #     if c != self:
        #         c.message(line)

    def message(self, message):
        self.transport.write(message)

    def dropConnection(self):
        #self.myError.UserError(string='drop connection from server due to silence')
        log.msg( "Drop connection from server due to silence{}".format(self.transport.getPeer()) )
        self.transport.loseConnection()



factory = protocol.ServerFactory()
factory.protocol = MyChat
factory.clients = []

application = service.Application("chatserver")
internet.TCPServer(port, factory).setServiceParent(application)