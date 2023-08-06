import unittest

from sample.common.logger import Logger
from sample.pom.harness import Harness
from sample.pom.page1_pom import Page1Pom
from sample.pom.root_pom import RootPom


# -------------------
class TestGui(unittest.TestCase):
    th = Harness()
    root = None
    page1 = None
    logger = None

    # --------------------
    @classmethod
    def setUpClass(cls):
        cls.logger = Logger()
        cls.th.init(cls.logger)
        cls.page1 = Page1Pom(cls.th)
        cls.root = RootPom(cls.th)

    # -------------------
    def setUp(self):
        print('')

    # -------------------
    def tearDown(self):
        self.root.kill_process(self)

    # --------------------
    @classmethod
    def tearDownClass(cls):
        cls.th.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_overall(self):
        self.root.start_process(self.logger, self)

        # connect to GUI App
        self.th.connect()
        self.assertTrue(self.th.is_connected())

        # get page content
        self.th.get_screen()
        # uncomment to debug
        # self.logger.info(f'current screen: {json.dumps(self.th.content, indent=4)}')

        # check titles for their contents
        self.assertEqual(self.root.title, 'Sample Version: v1.0.1')
        self.assertEqual(self.page1.title, 'Page : ')

        # check correct page number
        self.assertEqual(self.page1.page_number, 'page1')

        # check button state and text
        self.assertEqual(self.page1.button1_state, 'normal')
        self.assertEqual(self.page1.button1_text, 'press me!')
        self.assertEqual(self.page1.button2_state, 'normal')
        self.assertEqual(self.page1.button2_text, 'press me!')

        # check initial label text
        self.assertEqual(self.page1.label1_text, 'state: 0')
        self.assertEqual(self.page1.label2_text, 'state: 0')

        # click on button1 and see if label1 changes from 0 to 1
        self.page1.click_button1()
        self.th.get_screen()
        self.assertEqual(self.page1.label1_text, 'state: 1')
        self.assertEqual(self.page1.label2_text, 'state: 0')

        # click on button2 and see if label2 changes from 0 to 1
        self.page1.click_button2()
        self.th.get_screen()
        self.assertEqual(self.page1.label1_text, 'state: 1')
        self.assertEqual(self.page1.label2_text, 'state: 1')

        # menu clear should reset both states to 0
        self.root.click_menu_clear()
        self.th.get_screen()
        self.assertEqual(self.page1.label1_text, 'state: 0')
        self.assertEqual(self.page1.label2_text, 'state: 0')

        # menu: File | later
        self.root.click_menu_file_later()
        # TODO check to see if it worked

        self.th.cmd01()

        # menu: File | Exit
        # self.root.click_menu_file_exit()
