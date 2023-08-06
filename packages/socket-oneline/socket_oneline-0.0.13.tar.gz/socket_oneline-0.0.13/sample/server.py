import time

from sample.services import Services
from socket_oneline import OnelineServer


# --------------------
## sample Server that wraps the OnelineServer
class Server:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to the Oneline Server
        self._server = OnelineServer()

    # --------------------
    ## initialize
    # Start the OnelineServer
    #
    # @return None
    def init(self):
        Services.logger.info(f'server      : started version:v{self._server.version}')

        self._server.callback = self._callback
        self._server.ip_address = Services.ip_address
        self._server.ip_port = Services.ip_port
        self._server.logger = Services.logger
        self._server.verbose = Services.verbose
        if not self._server.start():
            Services.logger.info('ERR failed to set params')
            return
        # TODO convert to wait_until... with timeout
        time.sleep(0.1)

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        pass

    # --------------------
    ## wait until the server stops running i.e. it is shutdown
    #
    # @return None
    def wait_until_done(self):
        while self._server.is_running:
            time.sleep(0.5)

    # --------------------
    ## callback function used by OnelineServer to handle incoming commands
    #
    # @param cmd         the incoming command from the client
    # @param is_invalid  indicates if the command was invalid
    # @return None
    def _callback(self, cmd, is_invalid):
        Services.logger.info(f'server      : callback: cmd="{cmd}" is_invalid={is_invalid}')
        if cmd == 'cmd01':
            self._server.send('ack')
        else:
            # unknown command, let client know
            self._server.send('nak - unknown cmd')
