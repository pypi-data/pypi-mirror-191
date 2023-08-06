# --------------------
## simulates a logger instance
class Logger:
    # --------------------
    ## initialize
    def __init__(self):
        pass

    # --------------------
    ## write the message to stdout and save to the array for later processing
    #
    # @param msg  the message to log
    # @return None
    def info(self, msg):
        print(f'INFO {msg}')
