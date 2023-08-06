import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.constants import Constants
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp003(unittest.TestCase):
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
    def test_tp003(self):
        pth.proto.protocol('tp-003', 'check "click_left_at" with an invalid values')
        pth.proto.add_objective('check that click_left_at() respond with accurate nak json objects')
        pth.proto.add_objective('check that click_left_on() respond with accurate nak json objects')
        pth.proto.add_objective('check that click_left() respond with accurate nak json objects')
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

        pth.proto.step('get page content and confirm initial state is "state: 0"')
        services.th.get_screen()
        pth.ver.verify_gt(len(services.th.content), 0)
        label1_path = ['window1', 'page1_frame', 'button_frame', 'label1']
        label1 = services.th.search(label1_path)
        pth.ver.verify_equal('state: 0', label1['value'], reqids=['SRS-051'])

        pth.proto.step('search using a valid path to button1')
        button_path = ['window1', 'page1_frame', 'button_frame', 'button1']
        button = services.th.search(button_path)
        pth.ver.verify_equal('press me!', button['value'])

        # === click_left_on()
        pth.proto.step('click_left_on() on button1 using item returned from search')
        ack_nak = services.th.click_left_on(button)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label1 has changed to "state: 1"')
        services.th.get_screen()
        label1 = services.th.search(label1_path)
        pth.ver.verify_equal('state: 1', label1['value'], reqids=['SRS-051'])

        # === click_left()
        pth.proto.step('click_left() on button1 using search path')
        ack_nak = services.th.click_left(button_path)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label1 has changed to "state: 0"')
        services.th.get_screen()
        label1 = services.th.search(label1_path)
        pth.ver.verify_equal('state: 0', label1['value'], reqids=['SRS-051'])

        # === click_left_at()
        pth.proto.step('click_left_at() on button1 using raw x, y coordinates')
        button = services.th.search(button_path)
        x = int((button['coordinates']['x1'] + button['coordinates']['x2']) / 2)
        y = int((button['coordinates']['y1'] + button['coordinates']['y2']) / 2)
        ack_nak = services.th.click_left_at(x, y)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label1 has changed to "state: 1"')
        services.th.get_screen()
        label1 = services.th.search(label1_path)
        pth.ver.verify_equal('state: 1', label1['value'], reqids=['SRS-051'])

        # === click_left_on()
        pth.proto.step('click_left_on() with None item')
        ack_nak = services.th.click_left_on(None)
        pth.ver.verify_equal('click_left_on', ack_nak['rsp'], reqids=['SRS-053'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-053'])
        pth.ver.verify_equal('click item is None', ack_nak['reason'], reqids=['SRS-053'])

        pth.proto.step('click_left_on() with missing coordinates')
        ack_nak = services.th.click_left_on({})
        pth.ver.verify_equal('click_left_on', ack_nak['rsp'], reqids=['SRS-053'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-053'])
        pth.ver.verify_equal('click item missing coordinates values', ack_nak['reason'], reqids=['SRS-053'])

        # === click_left()
        pth.proto.step('click_left() with None path')
        ack_nak = services.th.click_left(None)
        pth.ver.verify_equal('click_left', ack_nak['rsp'], reqids=['SRS-052'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-052'])
        pth.ver.verify_equal('click path is None', ack_nak['reason'], reqids=['SRS-052'])

        pth.proto.step('click_left() with empty path')
        ack_nak = services.th.click_left([])
        pth.ver.verify_equal('click_left', ack_nak['rsp'], reqids=['SRS-052'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-052'])
        pth.ver.verify_equal('click path is empty', ack_nak['reason'], reqids=['SRS-052'])

        pth.proto.step('click_left() with unknown path')
        ack_nak = services.th.click_left(['windowx1'])
        pth.ver.verify_equal('click_left', ack_nak['rsp'], reqids=['SRS-052'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-052'])
        pth.ver.verify_equal('search path is not found', ack_nak['reason'], reqids=['SRS-052'])

        # === click_left_at()
        pth.proto.step('click_left_at() with bad x coordinate')
        ack_nak = services.th.click_left_at(1.23, 10)
        pth.ver.verify_equal('click_left_at', ack_nak['rsp'], reqids=['SRS-054'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-054'])
        pth.ver.verify_equal('click x-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-054'])

        pth.proto.step('click_left_at() with bad y coordinate')
        ack_nak = services.th.click_left_at(10, 1.23)
        pth.ver.verify_equal('click_left_at', ack_nak['rsp'], reqids=['SRS-054'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-054'])
        pth.ver.verify_equal('click y-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-054'])

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
