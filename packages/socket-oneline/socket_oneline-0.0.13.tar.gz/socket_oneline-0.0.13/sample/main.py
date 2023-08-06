import os
import time

from sample.client import Client
from sample.cmd_runner import CmdRunner
from sample.logger import Logger
from sample.services import Services


# --------------------
## sample App to set up a background process to run the OnelineServer and
# to run the OnelineClient locally
class App:
    # --------------------
    ## constructor
    def __init__(self):
        ## when done indicates all done with the bg process
        self._finished = False

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        Services.logger = Logger()

        # TODO handle Ctrl-C
        # TODO check if server came down cleanly or threw excp; how?
        crunner = CmdRunner()
        path = os.path.join('sample', 'server_main.py')
        cmd = f'python -u {path}'
        crunner.start_task_bg('server proc', cmd, self.run_fn, working_dir='.')
        time.sleep(0.5)

    # --------------------
    ## run the client for various scenarios
    #
    # @return None
    def run(self):
        # server is up, talk to it with a client
        client = Client()
        client.init()
        # confirm the server is up and working
        client.ping()
        # send a known cmd, expect 'ack' in return
        client.cmd01()
        # send an unknown cmd, expect 'nak' in return
        client.send_recv('junk')
        # let the server know we're about to disconnect
        client.disconnect()
        client.term()

        # create a new client
        client = Client()
        client.init()
        client.ping()
        # tell server to exit, stop the process
        client.shutdown()
        client.term()

        self._finished = True

    # --------------------
    ## callback to handle bg process that holds the OnelineServer
    #
    # @param proc  the Popen process handle
    # @return True if this should be called again, False otherwise
    def run_fn(self, proc):
        line = ''
        while True:
            ch = proc.stdout.read(1)
            if ch in ['\n', '\x0A']:
                break
            line += ch
        print(line)

        if self._finished:
            return False

        return True


# --------------------
## mainline
def main():
    app = App()
    app.init()
    app.run()


# --------------------
if __name__ == '__main__':
    main()
