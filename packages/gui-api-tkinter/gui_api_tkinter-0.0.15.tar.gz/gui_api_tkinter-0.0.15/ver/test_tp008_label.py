import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.constants import Constants
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp008(unittest.TestCase):
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
    def test_tp008(self):
        pth.proto.protocol('tp-008', 'check "set_text" function')
        pth.proto.add_objective('check that set_text() correctly sets text in an Entry widget')
        pth.proto.add_objective('check that set_text() respond with accurate nak json objects')
        pth.proto.add_objective('check that set_text_on() correctly sets text in an Entry widget')
        pth.proto.add_objective('check that set_text_on() respond with accurate nak json objects')
        pth.proto.add_objective('check that set_text_at() correctly sets text in an Entry widget')
        pth.proto.add_objective('check that set_text_at() respond with accurate nak json objects')
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

        pth.proto.step('check initial Entry widget information')
        entry_path = ['window1', 'page1_frame', 'button_frame', 'entry1']
        item = services.th.search(entry_path)
        pth.ver.verify_equal('Entry', item['class'])
        pth.ver.verify_equal('entry1', item['name'], reqids=['SRS-090'])
        pth.ver.verify_equal('', item['value'], reqids='SRS-090')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-090')

        # === set_text_on
        msg = 'abcd'
        pth.proto.step('enter a string into the Entry widget')
        services.th.set_text_on(item, msg)
        services.th.get_screen()

        pth.proto.step('verify the contents of the Entry widget have changed')
        item = services.th.search(entry_path)
        pth.ver.verify_equal('Entry', item['class'])
        pth.ver.verify_equal('entry1', item['name'])
        pth.ver.verify_equal(msg, item['value'], reqids=['SRS-092', 'SRS-091'])
        pth.ver.verify_equal('normal', item['state'])

        # TODO fails, need a way to clear the contents of the widget; try w.delete(0, 'end')
        # msg = 'ghi'
        # pth.proto.step('enter a shorter string into the Entry widget')
        # services.th.set_text_on(item, msg)
        # services.th.get_screen()
        #
        # pth.proto.step('verify the contents of the Entry widget have changed')
        # item = services.th.search(entry_path)
        # pth.ver.verify_equal('Entry', item['class'])
        # pth.ver.verify_equal('entry1', item['name'])
        # pth.ver.verify_equal(msg, item['value'], reqids=['SRS-092', 'SRS-091'])
        # pth.ver.verify_equal('normal', item['state'])

        # # === set_text()
        pth.proto.step('set_text() on button1 using search path')
        ack_nak = services.th.set_text(entry_path, 'e')
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the Entry widget have changed to "abcde"')
        services.th.get_screen()
        item = services.th.search(entry_path)
        pth.ver.verify_equal('abcde', item['value'], reqids=['SRS-092', 'SRS-091'])

        # === set_text_at()
        pth.proto.step('set_text_at() on button1 using raw x, y coordinates')
        button = services.th.search(entry_path)
        x = int((button['coordinates']['x1'] + button['coordinates']['x2']) / 2)
        y = int((button['coordinates']['y1'] + button['coordinates']['y2']) / 2)
        ack_nak = services.th.set_text_at(x, y, 'f')
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the Entry widget have changed to "abcdef"')
        services.th.get_screen()
        item = services.th.search(entry_path)
        pth.ver.verify_equal('abcdef', item['value'], reqids=['SRS-092', 'SRS-091'])

        # === set_text_on()
        pth.proto.step('set_text_on() with None item')
        ack_nak = services.th.set_text_on(None, 'g')
        pth.ver.verify_equal('set_text_on', ack_nak['rsp'], reqids=['SRS-094'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-094'])
        pth.ver.verify_equal('set text item is None', ack_nak['reason'], reqids=['SRS-094'])

        pth.proto.step('set_text_on() with missing coordinates')
        ack_nak = services.th.set_text_on({}, 'h')
        pth.ver.verify_equal('set_text_on', ack_nak['rsp'], reqids=['SRS-094'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-094'])
        pth.ver.verify_equal('set text item missing coordinates values', ack_nak['reason'], reqids=['SRS-094'])

        pth.proto.step('set_text_on() with None message')
        ack_nak = services.th.set_text_on(item, None)
        pth.ver.verify_equal('set_text_on', ack_nak['rsp'], reqids=['SRS-094'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-094'])
        pth.ver.verify_equal('set text msg is None', ack_nak['reason'], reqids=['SRS-094'])

        pth.proto.step('set_text_on() with empty message')
        ack_nak = services.th.set_text_on(item, '')
        pth.ver.verify_equal('set_text_on', ack_nak['rsp'], reqids=['SRS-094'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-094'])
        pth.ver.verify_equal('set text msg is empty', ack_nak['reason'], reqids=['SRS-094'])

        # === set_text()
        pth.proto.step('set_text() with None path')
        ack_nak = services.th.set_text(None, 'i')
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('set text path is None', ack_nak['reason'], reqids=['SRS-093'])

        pth.proto.step('set_text() with empty path')
        ack_nak = services.th.set_text([], 'j')
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('set text path is empty', ack_nak['reason'], reqids=['SRS-093'])

        pth.proto.step('set_text() with unknown path')
        ack_nak = services.th.set_text(['windowx1'], 'k')
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('search path is not found', ack_nak['reason'], reqids=['SRS-093'])

        pth.proto.step('set_text() with None message')
        ack_nak = services.th.set_text(['window1'], None)
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('set text msg is None', ack_nak['reason'], reqids=['SRS-093'])

        pth.proto.step('set_text() with empty message')
        ack_nak = services.th.set_text(['window1'], '')
        pth.ver.verify_equal('set_text', ack_nak['rsp'], reqids=['SRS-093'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-093'])
        pth.ver.verify_equal('set text msg is empty', ack_nak['reason'], reqids=['SRS-093'])

        # === set_text_at()
        pth.proto.step('set_text_at() with bad x coordinate')
        ack_nak = services.th.set_text_at(1.23, 10, 'l')
        pth.ver.verify_equal('set_text_at', ack_nak['rsp'], reqids=['SRS-095'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-095'])
        pth.ver.verify_equal('set text x-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-095'])

        pth.proto.step('set_text_at() with bad y coordinate')
        ack_nak = services.th.set_text_at(10, 1.23, 'm')
        pth.ver.verify_equal('set_text_at', ack_nak['rsp'], reqids=['SRS-095'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-095'])
        pth.ver.verify_equal('set text y-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-095'])

        pth.proto.step('set_text_at() with None message')
        ack_nak = services.th.set_text_at(10, 20, None)
        pth.ver.verify_equal('set_text_at', ack_nak['rsp'], reqids=['SRS-095'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-095'])
        pth.ver.verify_equal('set text msg is None', ack_nak['reason'], reqids=['SRS-095'])

        pth.proto.step('set_text_at() with empty message')
        ack_nak = services.th.set_text_at(10, 20, '')
        pth.ver.verify_equal('set_text_at', ack_nak['rsp'], reqids=['SRS-095'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-095'])
        pth.ver.verify_equal('set text msg is empty', ack_nak['reason'], reqids=['SRS-095'])

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
