import unittest

from pytest_ver import pth

from gui_api_tkinter.lib.constants import Constants
from gui_api_tkinter.lib.harness.gui_api_harness import GuiApiHarness
from ver.helpers import services
from ver.helpers.helper import Helper
from ver.helpers.logger_mock import Logger


# -------------------
class TestTp010(unittest.TestCase):
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
    def test_tp010(self):
        pth.proto.protocol('tp-010', 'check "lbox_select" function')
        pth.proto.add_objective('check that lbox_select() correctly sets option in a Listbox widget')
        pth.proto.add_objective('check that lbox_select() respond with accurate nak json objects')
        pth.proto.add_objective('check that lbox_select_on() correctly sets option in a Listbox widget')
        pth.proto.add_objective('check that lbox_select_on() respond with accurate nak json objects')
        pth.proto.add_objective('check that lbox_select_at() correctly sets option in a Listbox widget')
        pth.proto.add_objective('check that lbox_select_at() respond with accurate nak json objects')
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

        pth.proto.step('check initial Lisbox widget information')
        lbox_path = ['window1', 'page1_frame', 'button_frame', 'listbox1']
        item = services.th.search(lbox_path)
        pth.ver.verify_equal('Listbox', item['class'])
        pth.ver.verify_equal('listbox1', item['name'], reqids=['SRS-110'])
        pth.ver.verify_equal(['lbox_item1', 'lbox_item2', 'lbox_item3', 'lbox_item4'],
                             item['value'], reqids='SRS-110')
        pth.ver.verify_equal('normal', item['state'], reqids='SRS-110')

        label3_path = ['window1', 'page1_frame', 'button_frame', 'label3']

        # === lbox_select_on
        opt_id = 1  # lbox_item2
        pth.proto.step('select an option on the Listbox widget')
        item = services.th.search(lbox_path)
        services.th.lbox_select_on(item, opt_id)

        pth.proto.step('verify the contents of the label3 widget have changed to "lbox_item2"')
        services.th.get_screen()
        label3 = services.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item2', label3['value'], reqids=['SRS-111', 'SRS-112'])

        opt_id = [2]  # lbox_item3
        pth.proto.step('select another option on the Listbox widget')
        item = services.th.search(lbox_path)
        services.th.lbox_select_on(item, opt_id)

        pth.proto.step('verify the contents of the label3 widget have changed to "lbox_item3"')
        services.th.get_screen()
        label3 = services.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item3', label3['value'], reqids=['SRS-111', 'SRS-112'])

        # === lbox_select()
        opt_id = 3  # lbox_item4
        pth.proto.step('lbox_select() on lbox1 using search path')
        ack_nak = services.th.lbox_select(lbox_path, opt_id)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the contents of the label3 widget have changed to "lbox_item4"')
        services.th.get_screen()
        label3 = services.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item4', label3['value'], reqids=['SRS-111', 'SRS-112'])

        # === lbox_select_at()
        pth.proto.step('lbox_select_at() on lbox1 using raw x, y coordinates')
        lbox = services.th.search(lbox_path)
        x = int((lbox['coordinates']['x1'] + lbox['coordinates']['x2']) / 2)
        y = int((lbox['coordinates']['y1'] + lbox['coordinates']['y2']) / 2)
        ack_nak = services.th.lbox_select_at(x, y, 1)
        pth.ver.verify_equal('ack', ack_nak['value'])

        pth.proto.step('verify the selected option is "lbox_item2"')
        services.th.get_screen()
        item = services.th.search(label3_path)
        pth.ver.verify_equal('lbox: lbox_item2', item['value'], reqids=['SRS-111', 'SRS-112'])

        # === lbox_select_on()
        pth.proto.step('lbox_select_on() with None item')
        ack_nak = services.th.lbox_select_on(None, 3)
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select item is None', ack_nak['reason'], reqids=['SRS-114'])

        pth.proto.step('lbox_select_on() with missing coordinates')
        ack_nak = services.th.lbox_select_on({}, 'h')
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select item missing coordinates values', ack_nak['reason'], reqids=['SRS-114'])

        pth.proto.step('lbox_select_on() with None opt_ids')
        ack_nak = services.th.lbox_select_on(item, None)
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select opt_ids is None', ack_nak['reason'], reqids=['SRS-114'])

        pth.proto.step('lbox_select_on() with empty opt_ids')
        ack_nak = services.th.lbox_select_on(item, 0)
        pth.ver.verify_equal('lbox_select_on', ack_nak['rsp'], reqids=['SRS-114'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-114'])
        pth.ver.verify_equal('lbox select opt_ids is empty', ack_nak['reason'], reqids=['SRS-114'])

        # === lbox_select()
        pth.proto.step('lbox_select() with None path')
        ack_nak = services.th.lbox_select(None, 1)
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select path is None', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with empty path')
        ack_nak = services.th.lbox_select([], 2)
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select path is empty', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with unknown path')
        ack_nak = services.th.lbox_select(['windowx1'], [3])
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('search path is not found', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with None opt_ids')
        ack_nak = services.th.lbox_select(['window1'], None)
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select opt_ids is None', ack_nak['reason'], reqids=['SRS-113'])

        pth.proto.step('lbox_select() with empty opt_ids')
        ack_nak = services.th.lbox_select(['window1'], [])
        pth.ver.verify_equal('lbox_select', ack_nak['rsp'], reqids=['SRS-113'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-113'])
        pth.ver.verify_equal('lbox select opt_ids is empty', ack_nak['reason'], reqids=['SRS-113'])

        # === lbox_select_at()
        pth.proto.step('lbox_select_at() with bad x coordinate')
        ack_nak = services.th.lbox_select_at(1.23, 10, 1)
        pth.ver.verify_equal('lbox_select_at', ack_nak['rsp'], reqids=['SRS-115'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-115'])
        pth.ver.verify_equal('lbox select x-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-115'])

        pth.proto.step('lbox_select_at() with bad y coordinate')
        ack_nak = services.th.lbox_select_at(10, 1.23, 2)
        pth.ver.verify_equal('lbox_select_at', ack_nak['rsp'], reqids=['SRS-115'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-115'])
        pth.ver.verify_equal('lbox select y-coordinate is not an integer', ack_nak['reason'], reqids=['SRS-115'])

        pth.proto.step('lbox_select_at() with None opt_ids')
        ack_nak = services.th.lbox_select_at(10, 20, None)
        pth.ver.verify_equal('lbox_select_at', ack_nak['rsp'], reqids=['SRS-115'])
        pth.ver.verify_equal('nak', ack_nak['value'], reqids=['SRS-115'])
        pth.ver.verify_equal('lbox select opt_ids is None', ack_nak['reason'], reqids=['SRS-115'])

        pth.proto.step('disconnect from GUI API server')
        services.helper.clean_shutdown()
        pth.ver.verify_false(services.th.is_connected())
