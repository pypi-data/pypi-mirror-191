from sample.logger import Logger
from sample.server import Server
from sample.services import Services


# --------------------
## mainline
# runs the OnelineServer wrapper
def main():
    Services.logger = Logger()

    server = Server()
    server.init()

    server.wait_until_done()
    server.term()


# --------------------
if __name__ == '__main__':
    main()
