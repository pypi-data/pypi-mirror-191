import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.constants import Constants
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp009(unittest.TestCase):
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
    def test_tp009(self):
        pth.proto.protocol('tp-009', 'check "click" on Radiobutton widgets')
        pth.proto.add_objective('check that Radiobutton widgets are correctly shown in screen content')
        pth.proto.add_objective('check that left mouse click functions work correctly on Radiobuttons')
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

        pth.proto.step('check initial Radiobutton widget information')
        rb1_path = ['window1', 'page1_frame', 'button_frame', 'rb1']
        rb1 = services.th.search(rb1_path)
        pth.ver.verify_equal('Radiobutton', rb1['class'])
        pth.ver.verify_equal('rb1', rb1['name'], reqids='SRS-100')
        pth.ver.verify_equal('option1', rb1['value'], reqids='SRS-100')
        pth.ver.verify_equal('normal', rb1['state'], reqids='SRS-100')

        rb2_path = ['window1', 'page1_frame', 'button_frame', 'rb2']
        rb2 = services.th.search(rb2_path)
        pth.ver.verify_equal('Radiobutton', rb2['class'])
        pth.ver.verify_equal('rb2', rb2['name'], reqids=['SRS-100'])
        pth.ver.verify_equal('option2', rb2['value'], reqids='SRS-100')
        pth.ver.verify_equal('normal', rb2['state'], reqids='SRS-100')

        rb3_path = ['window1', 'page1_frame', 'button_frame', 'rb3']
        rb3 = services.th.search(rb3_path)
        pth.ver.verify_equal('Radiobutton', rb3['class'])
        pth.ver.verify_equal('rb3', rb3['name'], reqids=['SRS-100'])
        pth.ver.verify_equal('option3', rb3['value'], reqids=['SRS-100'])
        pth.ver.verify_equal('normal', rb3['state'], reqids=['SRS-100'])

        label2_path = ['window1', 'page1_frame', 'button_frame', 'label2']
        label2 = services.th.search(label2_path)
        pth.ver.verify_equal('Label', label2['class'])
        pth.ver.verify_equal('label2', label2['name'], reqids=['SRS-100'])
        pth.ver.verify_equal('rb: notset', label2['value'], reqids=['SRS-100'])
        pth.ver.verify_equal('normal', label2['state'], reqids=['SRS-100'])

        # === click_left_on()
        pth.proto.step('click_left_on() on radiobutton1 using item returned from search')
        ack_nak = services.th.click_left_on(rb1)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label2 has changed to "rb: 1"')
        services.th.get_screen()
        label2 = services.th.search(label2_path)
        pth.ver.verify_equal('rb: 1', label2['value'], reqids=['SRS-100'])

        # === click_left()
        pth.proto.step('click_left() on radiobutton2 using the path to the widget')
        ack_nak = services.th.click_left(rb2_path)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label2 has changed to "rb: 2"')
        services.th.get_screen()
        label2 = services.th.search(label2_path)
        pth.ver.verify_equal('rb: 2', label2['value'], reqids=['SRS-100'])

        # === click_left_at()
        pth.proto.step('click_left_at() on radiobutton3 using x,y coordinates')
        item = services.th.search(rb3_path)
        coord = item['coordinates']
        x = int((coord['x1'] + coord['x2']) / 2)
        y = int((coord['y1'] + coord['y2']) / 2)
        ack_nak = services.th.click_left_at(x, y)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('confirm label2 has changed to "rb: 3"')
        services.th.get_screen()
        label2 = services.th.search(label2_path)
        pth.ver.verify_equal('rb: 3', label2['value'], reqids=['SRS-100'])

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
