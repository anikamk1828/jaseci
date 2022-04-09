from jaseci.utils.mem_hook import mem_hook
from jaseci.actor.sentinel import sentinel
from jaseci.graph.graph import graph
from jaseci.element.super_master import super_master
from jaseci.element.master import master
from jaseci.utils.utils import TestCaseHelper
from unittest import TestCase
import jaseci.tests.jac_test_progs as jtp


class jac_tests(TestCaseHelper, TestCase):
    """Unit tests for Jac language"""

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_bug_check1(self):
        gph = graph(m_id='anon', h=mem_hook())
        sent = sentinel(m_id='anon', h=gph._h)
        sent.register_code(jtp.bug_check1)
        test_walker = \
            sent.walker_ids.get_obj_by_name('init')
        test_walker.prime(gph)
        test_walker.run()
        report = test_walker.report
        self.assertEqual(report[0][0], "THIS IS AN INTENT_LABEL")

    def test_action_load_std_lib(self):
        mast = super_master(h=mem_hook())
        mast.sentinel_register(name='test', code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name='walker_run', params={'name': 'aload'})['report']
        self.assertEqual(report[0], True)

    def test_action_load_std_lib_only_super(self):
        mast = master(h=mem_hook())
        mast.sentinel_register(name='test', code=jtp.action_load_std_lib)
        report = mast.general_interface_to_api(
            api_name='walker_run', params={'name': 'aload'})
        report = report['report']
        self.assertEqual(report[0], False)
