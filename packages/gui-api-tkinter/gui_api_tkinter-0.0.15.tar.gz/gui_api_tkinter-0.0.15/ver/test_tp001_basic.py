import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.constants import Constants
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp001(unittest.TestCase):
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
    def test_tp001(self):
        pth.proto.protocol('tp-001', 'basic server tests')
        pth.proto.add_objective('check server connect and disconnect')
        pth.proto.add_objective('check get_screen gets screen content of GUI')
        pth.proto.add_objective('check click successfully clicks a button')
        pth.proto.add_objective('check menu items can be invoked')
        pth.proto.add_objective('check callback function can be invoked')
        pth.proto.add_precondition('do_install has been run')
        pth.proto.add_precondition('latest versions of all modules have been retrieved')
        pth.proto.set_dut_version(f'v{Constants.version}')

        pth.proto.step('start gui')
        services.helper.start_process()
        pth.ver.verify_true(services.helper.gui_process.is_alive())
        pth.ver.verify_false(services.th.is_connected(), reqids=['SRS-001', 'SRS-030'])

        pth.proto.step('connect harness to GUI App server')
        services.th.connect()
        pth.ver.verify_true(services.th.is_connected(), reqids=['SRS-001', 'SRS-004'])

        pth.proto.step('get page content')
        services.th.get_screen()
        pth.ver.verify_gt(len(services.th.content), 0, reqids=['SRS-020', 'SRS-032', 'SRS-021'])

        pth.proto.step('check initial state of the label')
        pth.ver.verify_equal(services.helper.label1_text, 'state: 0', reqids=['SRS-050', 'SRS-022', 'SRS-023'])

        pth.proto.step('click a button')
        services.helper.click_button1()
        services.th.get_screen()
        pth.ver.verify_equal(services.helper.label1_text, 'state: 1', reqids=['SRS-050', 'SRS-051'])

        pth.proto.step('click "Clear" menu item')
        services.helper.click_clear_menuitem()
        services.th.get_screen()
        pth.ver.verify_equal(services.helper.label1_text, 'state: 0', reqids=['SRS-060', 'SRS-062', 'SRS-061'])

        pth.proto.step('send "cmd01" command')
        cmd = {
            'cmd': 'cmd01',
            'param1': 'some parameter1',
            'param2': 'some parameter2',
        }
        rsp = services.th.send_recv(cmd)
        pth.ver.verify_equal(rsp['value'], 'ack', reqids=['SRS-010', 'SRS-032'])

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected(), reqids=['SRS-003', 'SRS-031'])
