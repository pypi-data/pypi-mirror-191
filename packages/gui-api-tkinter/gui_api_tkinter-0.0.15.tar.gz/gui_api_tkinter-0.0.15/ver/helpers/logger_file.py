import os
import time


# --------------------
## logger instance
class Logger:
    # --------------------
    ## initialize
    def __init__(self):
        ## holds count of the last time a flush was done
        self._flush_count = 0
        ## holds the last time a full DTS was written to the log
        self._start_time = 0

        self._path = os.path.join('out', 'ver_logger.txt')
        self._fp = None

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        self._fp = open(self._path, 'w')
        self.info('starting')

    # --------------------
    ## write the message to stdout and save to the array for later processing
    #
    # @param msg  the message to log
    # @return None
    def info(self, msg):
        self._log('INFO', msg)

    # --------------------
    ## log a line
    #
    # @param tag    what kind of log line is it
    # @param msg    the text of the log line
    # @return None
    def _log(self, tag, msg):
        elapsed = time.time() - self._start_time
        if elapsed > 3600:
            self._start_time = time.time()
            tstr = time.strftime("%H:%M:%S.{}".format(str(elapsed)[2:])[:12], time.localtime(self._start_time))
            self._fp.write(f'{tstr} {tag:<4} on {time.strftime("%Y/%m/%d", time.localtime(self._start_time))}\n')
            elapsed = time.time() - self._start_time

        tstr = time.strftime("%H:%M:%S.{}".format(str(elapsed)[2:])[:12], time.gmtime(elapsed))
        self._fp.write(f'{tstr} {tag:<4} {msg}\n')

        self._flush_count += 1
        if self._flush_count > 1:
            self._fp.flush()
            self._flush_count = 0
