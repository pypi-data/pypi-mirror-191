import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.constants import Constants
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp007(unittest.TestCase):
    page1 = None
    logger = None
    helper = None
    th = None

    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()

        services.th = GuiApiHarness()
        services.th.init()
        services.logger = Logger()
        services.helper = Helper()

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        services.helper.kill_process()
        self.assertFalse(services.helper.gui_process.is_alive())

        # uncomment for debugging
        # print(f'DBG {services.logger.lines}')

    # --------------------
    @classmethod
    def tearDownClass(cls):
        services.th.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp007(self):
        pth.proto.protocol('tp-007', 'check for an invalid menuitem')
        pth.proto.add_objective('check that menu_click() invokes menu items at various menu levels')
        pth.proto.add_objective('check that menu_click() responds with accurate nak json objects')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{Constants.version}')

        pth.proto.step('start gui')
        # don't call callback
        services.helper.start_process()
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected())

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected())

        pth.proto.step('get page content')
        services.th.get_screen()
        pth.ver.verify_gt(len(services.th.content), 0)

        # uncomment for debug
        # print(f'DBG {json.dumps(services.th.content, indent=4)}')

        pth.proto.step('press menu item: Clear menu item')
        menu_path = [2]  # path to the "Clear" menu item
        ack_nak = services.th.menu_click(menu_path)
        pth.ver.verify_equal('menu_click', ack_nak['rsp'], reqids=['SRS-062', 'SRS-061'])
        pth.ver.verify_equal('ack', ack_nak['value'], reqids=['SRS-062', 'SRS-061'])

        pth.proto.step('press menu item in 2 levels: File | later')
        menu_path = [1, 0]  # path to the "File | later" menu item
        ack_nak = services.th.menu_click(menu_path)
        pth.ver.verify_equal('menu_click', ack_nak['rsp'], reqids=['SRS-062', 'SRS-061'])
        pth.ver.verify_equal('ack', ack_nak['value'], reqids=['SRS-062', 'SRS-061'])

        pth.proto.step('check if single menuitem is not found')
        menu_path = [9]
        ack_nak = services.th.menu_click(menu_path)
        pth.ver.verify_equal('menu_click', ack_nak['rsp'], reqids=['SRS-062', 'SRS-061'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-063'])
        pth.ver.verify_equal('menuitem not found', ack_nak['reason'], reqids=['SRS-063'])

        pth.proto.step('check if last menu item is not found')
        menu_path = [1, 10]
        ack_nak = services.th.menu_click(menu_path)
        pth.ver.verify_equal('menu_click', ack_nak['rsp'], reqids=['SRS-062', 'SRS-061'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-063'])
        pth.ver.verify_equal('menuitem not found', ack_nak['reason'], reqids=['SRS-063'])

        pth.proto.step('check for empty menuitem list')
        menu_path = []
        ack_nak = services.th.menu_click(menu_path)
        pth.ver.verify_equal('menu_click', ack_nak['rsp'], reqids=['SRS-062', 'SRS-061'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-063'])
        pth.ver.verify_equal('menu path is empty', ack_nak['reason'], reqids=['SRS-063'])

        pth.proto.step('check if menuitem list is None')
        menu_path = None
        ack_nak = services.th.menu_click(menu_path)
        pth.ver.verify_equal('menu_click', ack_nak['rsp'], reqids=['SRS-062', 'SRS-061'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-063'])
        pth.ver.verify_equal('menu path is None', ack_nak['reason'], reqids=['SRS-063'])

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
