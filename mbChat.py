# -*- coding: utf-8 -*-

"""The most basic chat protocol possible.

sudo kill -TERM $(sudo cat chat.pid)
sudo twistd  --python=mbChat.py --pidfile=mbChat.pid --logfile=logs/mbChat.log

"""
port = 14210
delayBeforeDropConnection = 180


#from twisted.protocols import basic
from twisted.internet import protocol, reactor, error
from twisted.application import service, internet
from twisted.python import log


class MyChat(protocol.Protocol):
    def connectionMade(self):
        log.msg( "Got new client: {}".format(self.transport.getPeer()) )
        self.factory.clients.append(self)
        self.timeout = reactor.callLater(delayBeforeDropConnection, self.dropConnection)
        self.myError = error

    def connectionLost(self, reason):
        log.msg( "Lost a client! reason: {}".format(reason) )
        self.factory.clients.remove(self)

    def dataReceived(self, line):
        log.msg( "received {}".format( repr(line) ) )
        self.timeout.reset(delayBeforeDropConnection)
        for c in self.factory.clients:
            if c != self:
                c.message(line)

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