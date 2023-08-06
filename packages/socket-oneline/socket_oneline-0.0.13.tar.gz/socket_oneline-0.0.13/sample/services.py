# --------------------
## holds references to common values and objects
class Services:
    ## the IP address to use for socket comms
    ip_address = '127.0.0.1'
    ## the IP port to use for socket comms
    ip_port = 5001
    ## whether logging is verbose or not
    verbose = True
    ## reference to the logger
    logger = None
