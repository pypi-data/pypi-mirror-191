import json
import time

from socket_oneline import OnelineServer

from .. import services


# --------------------
## Server mainline to communication with the socket server
class GuiApiServer:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds reference to the Oneline Server
        self._olserver = OnelineServer()

    # --------------------
    ## initialize
    # Start the OnelineServer
    #
    # @return None
    def init(self):
        services.logger.info('server      : started')

        self._olserver.callback = self._callback
        self._olserver.ip_address = services.cfg.ip_address
        self._olserver.ip_port = services.cfg.ip_port
        self._olserver.verbose = services.cfg.verbose
        self._olserver.logger = services.logger

        if not self._olserver.start():
            services.logger.info('ERR failed to set params')
            return
        time.sleep(0.1)

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._olserver is not None:
            self._olserver.term()
            self._olserver = None

    # --------------------
    ## send an ack to the client
    #
    # @param cmd  the command this ack response is for
    # @return None
    def send_ack(self, cmd: dict):
        rsp = {
            'rsp': cmd,
            'value': 'ack',
        }
        self.send(rsp)

    # --------------------
    ## send an nak to the client
    #
    # @param cmd     the command this nak response is for
    # @param reason  the reason for the nak
    # @return None
    def send_nak(self, cmd: dict, reason: str):
        rsp = {
            'rsp': cmd,
            'value': 'nak',
            'reason': reason,
        }
        self.send(rsp)

    # --------------------
    ## send response/message to the client
    #
    # @param msg  the message to send (no newline needed)
    # @return None
    def send(self, msg: dict):
        self._olserver.send(json.dumps(msg))

    # --------------------
    ## callback function used by server to handle incoming commands
    #
    # @param command     the incoming command from the client
    # @param is_invalid  indicates if the command is invalid
    # @return None
    def _callback(self, command, is_invalid):
        # all commands sent here should be json
        cmd = json.loads(command)
        services.logger.info(f'server      : callback: cmd="{cmd["cmd"]}" is_invalid={is_invalid}')
        if is_invalid:
            return

        if cmd['cmd'] == 'get_screen':
            screen = services.guiapi.get_screen()
            screen['rsp'] = cmd['cmd']
            self.send(screen)
        elif cmd['cmd'] == 'click_left':
            rsp = services.guiapi.click_left(cmd)
            self.send(rsp)
        elif cmd['cmd'] == 'menu_click':
            rsp = services.guiapi.menu_invoke(cmd)
            self.send(rsp)
        elif cmd['cmd'] == 'set_text':
            rsp = services.guiapi.set_text(cmd)
            self.send(rsp)
        elif cmd['cmd'] == 'lbox_select':
            rsp = services.guiapi.lbox_select(cmd)
            self.send(rsp)
        elif services.cfg.callback is not None:
            rsp = services.cfg.callback(cmd)
            if rsp is None:
                self.send_ack(cmd['cmd'])
            else:
                rsp['rsp'] = cmd['cmd']
                self.send(rsp)
        else:
            # unknown command, let client know
            self.send_nak(cmd['cmd'], 'unknown command')
