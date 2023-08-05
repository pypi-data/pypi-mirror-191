""" INCOMPLETE unit tests for lisz_app_data portion of ae namespace """
import ast
import os
import shutil
from copy import deepcopy
from typing import Any, Callable, Optional, Tuple, Union, cast
import pytest

from ae.base import TESTS_FOLDER, read_file, write_file
from ae.files import read_file_text
from ae.gui_app import id_of_flow, MainAppBase
from ae.lisz_app_data import (FLOW_PATH_ROOT_ID, FLOW_PATH_TEXT_SEP, IMPORT_NODE_MAX_FILE_LEN, IMPORT_NODE_MAX_ITEMS,
                              NODE_FILE_EXT, NODE_FILE_PREFIX,
                              check_item_id, correct_item_id, flow_path_items_from_text, item_sel_filter,
                              item_unsel_filter,
                              LiszDataMixin)


class AppTest(LiszDataMixin, MainAppBase):
    """ app test class """

    def call_method_delayed(self, _delay: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ redirect to direct call for unit testing. """
        return self.call_method(callback, *args, **kwargs)

    def init_app(self, **kwargs) -> Tuple[Optional[Callable], Optional[Callable]]:
        """

        :param kwargs:
        :return:
        """
        return None, None

    def on_app_init(self):
        """ initialize needed app instance attributes with empty test default values. """
        super().on_app_init()
        self.root_node = []
        self.current_node_items = self.root_node
        self.filtered_indexes = []

    def on_app_start(self):
        """ needed to test call LiszDataMixin.on_start_up() because is mixed in after MainAppBase. """
        super().on_app_start()

    def refresh_node_widgets(self):
        """ redraw widgets for each item of the current node. """


class TestHelperFunctions:
    def test_check_item_id(self):
        assert check_item_id(cast(str, None))
        assert check_item_id('')
        assert check_item_id(FLOW_PATH_ROOT_ID)
        assert check_item_id(FLOW_PATH_TEXT_SEP)
        assert check_item_id(FLOW_PATH_ROOT_ID + 'x') == ""
        assert check_item_id(FLOW_PATH_TEXT_SEP + 'x')
        assert check_item_id('test_tst') == ""
        assert check_item_id('[test')
        assert check_item_id('{test')

    def test_correct_item_id(self):
        assert correct_item_id("") == ""
        assert correct_item_id("* tst") == "tst"
        assert correct_item_id("\t*\tid to test") == "id to test"
        assert correct_item_id(FLOW_PATH_ROOT_ID) != ""
        assert correct_item_id(FLOW_PATH_ROOT_ID) != FLOW_PATH_ROOT_ID
        assert FLOW_PATH_TEXT_SEP not in correct_item_id(FLOW_PATH_TEXT_SEP)
        assert FLOW_PATH_TEXT_SEP not in correct_item_id("abc" + FLOW_PATH_TEXT_SEP + "tst")
        assert correct_item_id(FLOW_PATH_TEXT_SEP) != ""
        assert correct_item_id(FLOW_PATH_TEXT_SEP) != FLOW_PATH_TEXT_SEP

    def test_flow_path_items_from_text(self):
        assert flow_path_items_from_text("") == ("", "", [])

        flow_path_text = "flow" + FLOW_PATH_TEXT_SEP + "path"

        dict_lit = "{'id': 'tst'}"
        assert flow_path_items_from_text(flow_path_text + "\n" + dict_lit) \
               == ("", flow_path_text, [ast.literal_eval(dict_lit)])

        list_lit = "[{'id': 'tst'}]"
        assert flow_path_items_from_text(flow_path_text + "\n" + dict_lit) \
               == ("", flow_path_text, ast.literal_eval(list_lit))

        assert flow_path_items_from_text("id1\nid2\nid3") == ("", "", [dict(id='id1'), dict(id='id2'), dict(id='id3')])
        assert flow_path_items_from_text("tst") == ("", "", [dict(id="tst")])
        assert flow_path_items_from_text("tst\ntst2") == ("", "", [{'id': 'tst'}, {'id': 'tst2'}])
        assert flow_path_items_from_text("tst\rtst2") == ("", "", [{'id': 'tst'}, {'id': 'tst2'}])
        assert flow_path_items_from_text("tst\r\ntst2") == ("", "", [{'id': 'tst'}, {'id': 'tst2'}])

        assert flow_path_items_from_text("{}") == ("", "", [{}])
        assert flow_path_items_from_text("{'id': '3'}") == ("", "", [{'id': '3'}])
        assert flow_path_items_from_text(repr(dict(id='a'))) == ("", "", [{'id': 'a'}])

        assert flow_path_items_from_text("[]") == ("", "", [])
        assert flow_path_items_from_text("[{'id': '3'}]") == ("", "", [{'id': '3'}])
        assert flow_path_items_from_text(repr([dict(id='a')])) == ("", "", [{'id': 'a'}])

    def test_flow_path_items_from_text_errors(self):
        # error but no exception if dict() get used instead of real dict literal (interpreted as item/leaf id)
        assert flow_path_items_from_text("dict(a=1, b=2)") == ("", "", [{'id': 'dict(a=1, b=2)'}])

        # empty list on syntax error
        assert flow_path_items_from_text("[") == ("unexpected EOF while parsing (<unknown>, line 1)", "", [])
        # assert flow_path_items_from_text("{") == ("unexpected EOF while parsing (<unknown>, line 1)", "", [])
        assert flow_path_items_from_text("{") == (
            "closing parenthesis ']' does not match opening parenthesis '{' (<unknown>, line 1)", "", [])

        # no exception but empty node returned if dict/list literals are erroneous
        assert flow_path_items_from_text("{wrong syntax") == ("invalid syntax (<unknown>, line 1)", "", [])
        assert flow_path_items_from_text("[wrong syntax") \
               == ("unexpected EOF while parsing (<unknown>, line 1)", "", [])

    def test_item_sel_filter(self):
        assert not item_sel_filter(dict(id='3'))
        assert item_sel_filter(dict(id='6', sel=1))
        assert not item_sel_filter(dict(id='9', node=[dict(id=12, sel=0)]))
        assert item_sel_filter(dict(id='9', node=[dict(id=12, sel=1)]))

    def test_item_unsel_filter(self):
        assert item_unsel_filter(dict(id='3'))
        assert not item_unsel_filter(dict(id='6', sel=1))
        assert item_unsel_filter(dict(id='9', node=[dict(id=12, sel=0)]))
        assert not item_unsel_filter(dict(id='9', node=[dict(id=12, sel=1)]))


class TestLiszDataMixin:
    def test_instantiation(self, restore_app_env):
        app = AppTest()
        assert app

    def test_add_item(self, restore_app_env):
        app = AppTest()
        assert not app.current_node_items

        assert app.add_item(dict(id='3')) == ""
        assert app.add_item(dict(id='6')) == ""
        assert app.add_item(dict(id='9', node=[dict(id='12')])) == ""

        assert app.current_node_items == [dict(id='9', node=[dict(id='12')]), dict(id='6'), dict(id='3')]

    def test_add_item_merge_and_change_to_node(self):
        app = AppTest()
        assert not app.current_node_items

        assert app.add_item(dict(id='3')) == ""
        assert app.add_item(dict(id='6')) == ""
        # duplicate node ids are ignored (only returning (ignorable) error if debug_level is set)
        assert app.add_item(dict(id='6', node=[dict(id='12')])) == ""
        # on duplicate leaf id add_item() is returning a error message
        assert not app.add_item(dict(id='6', node=[dict(id='12')])) == ""
        # again if we overwrite a leaf with a node of the same id then no error get returned (if debug_level is not set)
        assert app.add_item(dict(id='6', node=[dict(id='12', node=[])])) == ""

        assert app.current_node_items == [dict(id='6', node=[dict(id='12', node=[])]), dict(id='3')]

    def test_add_items(self, restore_app_env):
        app = AppTest()
        assert not app.current_node_items

        items = [dict(id='3'), dict(id='6'), dict(id='9', node=[dict(id='12')])]
        assert app.add_items(items) == ""
        assert app.current_node_items == items

        err_msg = app.add_items([dict(id='3')])
        assert err_msg
        assert '\n' not in err_msg

        err_msg = app.add_items([dict(id='3'), dict(id='3')])
        assert err_msg
        assert '\n' in err_msg

    @pytest.mark.parametrize("tst_node,expected", [
        (
            [dict(id='3', node=[
                dict(id='15', sel=1), dict(id='18'), dict(id='1s', node=[
                    dict(id='zzz'),
                ])
            ]), dict(id='x')
             ],
            [dict(id='3', sel=1.0, node=[
                dict(id='15', sel=1), dict(id='18', sel=1), dict(id='1s', sel=1.0, node=[
                    dict(id='zzz', sel=1),
                ])
            ]), dict(id='x', sel=1)
             ]
        )])
    def test_change_sub_node_sel_on(self, tst_node, expected, restore_app_env):
        app = AppTest()
        app.change_sub_node_sel(tst_node, True)
        assert tst_node == expected

    @pytest.mark.parametrize("tst_node,expected", [
        (
            [dict(id='3', node=[
                dict(id='15', sel=1), dict(id='18'), dict(id='1s', node=[
                    dict(id='zzz'),
                ])
            ]), dict(id='x')
             ],
            [dict(id='3', node=[
                dict(id='15'), dict(id='18'), dict(id='1s', node=[
                    dict(id='zzz'),
                ])
            ]), dict(id='x')
             ]
        )])
    def test_change_sub_node_sel_off(self, tst_node, expected, restore_app_env):
        app = AppTest()
        app.change_sub_node_sel(tst_node, False)
        assert tst_node == expected

    def test_delete_items_leaf(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='3'), dict(id='6'), dict(id='9'), ]
        app.delete_items('6')
        assert app.current_node_items == [dict(id='3'), dict(id='9'), ]

    def test_current_item_or_node_literal(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='3'), dict(id='6'), dict(id='9', node=[dict(id=12)]), ]

        assert app.current_item_or_node_literal().startswith('[')

        app.change_flow(id_of_flow('focus', 'item', '6'))
        assert app.current_item_or_node_literal() == '6'

        app.change_flow(id_of_flow('focus', 'item', '9'))
        assert app.current_item_or_node_literal().startswith('{')

    def test_delete_items_node(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='3'), dict(id='6', node=[dict(id='99'), ]), dict(id='9'), ]
        app.delete_items('6', node_only=True)
        assert app.current_node_items == [dict(id='3'), dict(id='6'), dict(id='9'), ]

    def test_edit_validate_add_new_cancel(self, restore_app_env):
        app = AppTest()
        assert app.edit_validate(-1, '') == ""
        assert len(app.current_node_items) == 0

        assert app.edit_validate(-1, '* ') == ""
        assert len(app.current_node_items) == 0

        assert app.edit_validate(-1, '\t- ') == ""
        assert len(app.current_node_items) == 0

        assert app.edit_validate(-1, ' \t-\t \t') == ""
        assert len(app.current_node_items) == 0

    def test_edit_validate_add_new_corrected(self, restore_app_env):
        app = AppTest()
        assert app.edit_validate(-1, FLOW_PATH_TEXT_SEP) == ""
        assert app.current_node_items[0]['id'] == "/"

        assert app.edit_validate(-1, "* tst") == ""
        assert app.current_node_items[0]['id'] == "tst"

        assert app.edit_validate(-1, "\t*\ttest id") == ""
        assert app.current_node_items[0]['id'] == "test id"

    def test_edit_validate_add_new_duplicate(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='3')]
        assert 'exists' in app.edit_validate(-1, '3')

    def test_edit_validate_add_new_leaf(self, restore_app_env):
        app = AppTest()
        app.current_node_items = []
        assert app.edit_validate(-1, '3') == ''
        assert app.current_node_items == [dict(id='3')]

    def test_edit_validate_add_new_node(self, restore_app_env):
        app = AppTest()
        app.current_node_items = []
        assert app.edit_validate(-1, '3', want_node=True) == ''
        assert app.current_node_items == [dict(id='3', node=[])]

    def test_edit_validate_edit_invalid(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='3'), dict(id='6')]
        assert ' cannot contain ' in app.edit_validate(1, ' / ')
        assert ' cannot contain ' in app.edit_validate(2, FLOW_PATH_TEXT_SEP)
        assert ' cannot contain ' in app.edit_validate(3, FLOW_PATH_TEXT_SEP + 'TST')

    def test_edit_validate_edit_duplicate(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='3'), dict(id='6')]
        assert 'exists' in app.edit_validate(0, '6')

    def test_edit_validate_edit_delete(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='3'), dict(id='6')]
        assert app.edit_validate(0, '') == 'request_delete_confirmation_for_item'
        assert app.current_node_items == [dict(id='3'), dict(id='6')]

    def test_edit_validate_edit_add_leaf(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='6')]
        assert app.edit_validate(0, '3') == ''
        assert app.current_node_items == [dict(id='3')]

    def test_edit_validate_edit_del_empty_node(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='6', node=[])]
        assert app.edit_validate(0, '3', want_node=False) == ''
        assert app.current_node_items == [dict(id='3')]

    def test_edit_validate_edit_del_node(self, restore_app_env):
        app = AppTest()
        app.current_node_items[:] = [dict(id='6', node=[dict(id='3')])]
        assert app.edit_validate(0, '3', want_node=False) == 'request_delete_confirmation_for_node'
        assert app.current_node_items == [dict(id='3', node=[dict(id='3')])]

    def test_edit_validate_edit_add_node(self, restore_app_env):
        app = AppTest()
        app.current_node_items = [dict(id='6')]
        assert app.edit_validate(0, '3', want_node=True) == ''
        assert app.current_node_items == [dict(id='3', node=[])]

    def test_export_node(self, restore_app_env):
        app = AppTest()

        assert app.export_node([], chr(0) + ', :invalid * < path >:')

        exp_file = os.path.join(TESTS_FOLDER, f'node_{FLOW_PATH_ROOT_ID}.txt')
        try:
            assert not app.export_node([], TESTS_FOLDER)
            assert os.path.exists(exp_file)
            assert read_file(exp_file) == "[]"
        finally:
            if os.path.exists(exp_file):
                os.remove(exp_file)

    def test_find_item_index(self, restore_app_env):
        app = AppTest()
        tid = 'tst_id'
        app.current_node_items = [dict(id=tid)]

        assert app.find_item_index(tid) == 0
        assert app.find_item_index('unknown_id') == -1

    def test_flow_key_text_with_any_action(self, restore_app_env):
        app = AppTest()
        flow_id = id_of_flow('action', 'obj')
        assert app.flow_key_text(flow_id, False) == (f".{flow_id}" if app.debug_level else "")

    def test_flow_key_text_with_focus_action(self, restore_app_env):
        app = AppTest()
        key = 'tst_key'
        tid = 'tst_id'
        flow_id = id_of_flow('focus', 'obj', key)

        app.current_node_items = []
        assert key[:3] in app.flow_key_text(flow_id, False)
        assert key[:6] in app.flow_key_text(flow_id, True)

        app.current_node_items = [dict(id=tid)]
        assert key[:5] in app.flow_key_text(flow_id, False)
        assert key[:6] in app.flow_key_text(flow_id, True)

        app.current_node_items.append(dict(id=key + "1"))
        assert key in app.flow_key_text(flow_id, False)
        assert key in app.flow_key_text(flow_id, True)

    def test_flow_path_from_text_empty(self, restore_app_env):
        app = AppTest()
        assert app.flow_path_from_text('') == []

    def test_flow_path_from_text_single(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[])]
        assert app.flow_path_from_text('3') == list((id_of_flow('enter', 'item', '3'),))

    def test_flow_path_from_text_deep(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[])])]
        assert app.flow_path_from_text('3' + FLOW_PATH_TEXT_SEP + '6') == list((id_of_flow('enter', 'item', '3'),
                                                                                id_of_flow('enter', 'item', '6'),))

    def test_flow_path_from_text_single_fix(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3')]
        assert app.flow_path_from_text('3') == []

    def test_flow_path_from_text_skip_check(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3')]
        assert app.flow_path_from_text('3' + FLOW_PATH_TEXT_SEP + '6', skip_check=True) == list(
            (id_of_flow('enter', 'item', '3'),
             id_of_flow('enter', 'item', '6'),))

    def test_flow_path_node(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='xx')])])]
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),
                                        id_of_flow('enter', 'item', '6'),))) == [{'id': 'xx'}]

    def test_flow_path_node_non_enter(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[])])]
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'), ))) == [{'id': '6', 'node': []}]
        assert app.flow_path_node(list((id_of_flow('xyz', 'item', '3'), ))) == app.root_node
        assert app.flow_path_node(list((id_of_flow('xyz', 'item', '3'),
                                        id_of_flow('enter', 'item', '6'), ))) == []

    def test_flow_path_node_fix_non_node(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6')])]
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),))) == [{'id': '6'}]
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),
                                        id_of_flow('enter', 'item', '6'),))) == []

    def test_flow_path_node_strict(self, restore_app_env):
        app = AppTest()
        tst_list = []
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=tst_list)])]
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),
                                        id_of_flow('enter', 'item', '6'),))) is tst_list

    def test_flow_path_node_repair_create(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = []
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),)), create=True) == []
        assert app.root_node == [dict(id='3', node=[])]

        app.root_node[:] = []
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),
                                        id_of_flow('enter', 'item', '6'),)), create=True) == []
        assert app.root_node == [dict(id='3', node=[dict(id='6', node=[])])]

        app.root_node[:] = [dict(id='3')]
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),
                                        id_of_flow('enter', 'item', '6'),)), create=True) == []
        assert app.root_node == [dict(id='3', node=[dict(id='6', node=[])])]

        app.root_node[:] = [dict(id='3', node=[dict(id='6')])]
        assert app.flow_path_node(list((id_of_flow('enter', 'item', '3'),
                                        id_of_flow('enter', 'item', '6'),)), create=True) == []
        assert app.root_node == [dict(id='3', node=[dict(id='6', node=[])])]

    def test_flow_path_quick_jump_nodes(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6')])]
        assert app.flow_path_quick_jump_nodes() == ['3']

    def test_flow_path_quick_jump_nodes_with_flow_path(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6')])]

        app.flow_path = []
        app.current_node_items = app.root_node
        assert app.flow_path_quick_jump_nodes() == ['3']

        app.flow_path = [id_of_flow('enter', 'item', '3'), ]
        app.current_node_items = app.root_node[0]['node']
        assert app.flow_path_quick_jump_nodes() == [FLOW_PATH_ROOT_ID]

        app.flow_path += [id_of_flow('open', 'anything'), id_of_flow('show', 'any_other')]
        app.current_node_items = app.root_node[0]['node']
        assert app.flow_path_quick_jump_nodes() == [FLOW_PATH_ROOT_ID]

    def test_flow_path_quick_jump_nodes_with_deep_flow_path(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.current_node_items = app.root_node[0]['node'][0]['node']
        app.flow_path = [id_of_flow('enter', 'item', '3'), id_of_flow('enter', 'item', '6'), ]
        assert app.flow_path_quick_jump_nodes() == [FLOW_PATH_ROOT_ID, '3']

        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9', node=[dict(id='12')])])])]
        app.current_node_items = app.root_node[0]['node'][0]['node']
        app.flow_path = [id_of_flow('enter', 'item', '3'), id_of_flow('enter', 'item', '6'), ]
        assert app.flow_path_quick_jump_nodes() == [FLOW_PATH_ROOT_ID, '3',
                                                    '3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9']

    def test_flow_path_text_fix_non_enter(self, restore_app_env):
        app = AppTest()
        assert app.flow_path_text([id_of_flow('show', 'item', '3')]) == ""

    def test_flow_path_text_shortening(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='69', node=[]), dict(id='696', node=[])])]
        app.flow_path = [id_of_flow('enter', 'item', '3'), id_of_flow('enter', 'item', '69'), ]
        assert app.flow_path_text(app.flow_path, min_len=1) == "3" + FLOW_PATH_TEXT_SEP + "69"

    def test_focus_neighbour_item_hit_end(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.filtered_indexes = (0, )
        app.flow_id = id_of_flow('focus', 'item', '3')
        app.focus_neighbour_item(1)
        assert app.flow_id == id_of_flow('focus', 'item', '3')

    def test_focus_neighbour_item_hit_begin(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.filtered_indexes = (0,)
        app.flow_id = id_of_flow('focus', 'item', '3')
        app.focus_neighbour_item(-1)
        assert app.flow_id == id_of_flow('focus', 'item', '3')

    def test_focus_neighbour_item_set_focus(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.filtered_indexes = (0, )
        app.flow_id = id_of_flow('')
        app.focus_neighbour_item(1)
        assert app.flow_id == id_of_flow('focus', 'item', '3')

    def test_focus_neighbour_item_focus_next(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='69', node=[dict(id='999')])]), dict(id='6')]
        app.filtered_indexes = (0, 1, )
        app.flow_id = id_of_flow('focus', 'item', '3')
        app.focus_neighbour_item(1)
        assert app.flow_id == id_of_flow('focus', 'item', '6')

    def test_focus_neighbour_item_focus_prev(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='0'), dict(id='3', node=[dict(id='69', node=[dict(id='999')])]), dict(id='6')]
        app.filtered_indexes = (0, 1, 2, )
        app.flow_id = id_of_flow('focus', 'item', '3')
        app.focus_neighbour_item(-1)
        assert app.flow_id == id_of_flow('focus', 'item', '0')

    def test_global_variables(self, restore_app_env):
        app = AppTest()
        assert 'FLOW_PATH_ROOT_ID' in app.global_variables()
        assert app.global_variables()['FLOW_PATH_ROOT_ID'] == FLOW_PATH_ROOT_ID

    def test_importable_node_files(self, restore_app_env):
        app = AppTest()

        name = 'check'
        imp_dir = os.path.join(TESTS_FOLDER, "import_dir")
        imp_file = os.path.join(imp_dir, f'node_{name}.txt')
        id1, id2 = 'test id to import', 'another item'
        node = [{'id': id1}, {'id': id2}]
        try:
            os.makedirs(imp_dir)
            write_file(imp_file, repr(node))
            node_file_info = app.importable_node_files(folder_path=imp_dir)
            assert len(node_file_info) == 1
            assert node_file_info[0] == (name, node, imp_file, "")
        finally:
            if os.path.exists(imp_dir):
                shutil.rmtree(imp_dir)

    def test_importable_node_files_empty_node(self, restore_app_env):
        app = AppTest()

        imp_dir = os.path.join(TESTS_FOLDER, "import_dir")
        imp_file = os.path.join(imp_dir, f'node_{FLOW_PATH_ROOT_ID}.txt')
        try:
            os.makedirs(imp_dir)
            write_file(imp_file, "[]")
            node_file_info = app.importable_node_files(folder_path=imp_dir)
            assert len(node_file_info) == 1
            assert node_file_info[0][:3] == (FLOW_PATH_ROOT_ID, [], imp_file)
            assert node_file_info[0][3]         # == error message: 'invalid file content or empty file'
        finally:
            if os.path.exists(imp_dir):
                shutil.rmtree(imp_dir)

    def test_importable_node_files_invalid_file(self, restore_app_env):
        app = AppTest()

        with pytest.raises(ValueError):
            app.importable_node_files(folder_path=chr(0) + ', :invalid * < path >:')

    def test_import_file_info(self, restore_app_env):
        app = AppTest()

        name = 'info'
        imp_file = os.path.join(TESTS_FOLDER, f'node_{name}.txt')
        id1, id2 = 'test id to import', 'another item'
        node = [{'id': id1}, {'id': id2}]
        try:
            write_file(imp_file, repr(node))
            node_file_info = app.import_file_info(imp_file)
            assert len(node_file_info) == 4
            assert node[0]['id'] == id1
            assert node[1]['id'] == id2
            assert node_file_info == (name, node, imp_file, "")
        finally:
            if os.path.exists(imp_file):
                os.remove(imp_file)

    def test_import_file_info_file_not_specified(self, restore_app_env):
        app = AppTest()

        name = 'info'
        imp_file = os.path.join(TESTS_FOLDER, f'node_{name}.txt')
        id1, id2 = 'test id to import', 'another item'
        node = [{'id': id1}, {'id': id2}]
        try:
            write_file(imp_file, repr(node))
            node_file_info = app.import_file_info(TESTS_FOLDER)  # missing file name
            assert len(node_file_info) == 4
            assert not node_file_info[1]
            assert node_file_info[3]
        finally:
            if os.path.exists(imp_file):
                os.remove(imp_file)

    def test_import_file_info_too_big(self, restore_app_env):
        app = AppTest()

        name = 'info'
        imp_file = os.path.join(TESTS_FOLDER, f'node_{name}.txt')
        item_lit = "{'id': 'test'}, "
        node_lit = "[" + item_lit * int(IMPORT_NODE_MAX_FILE_LEN / (len(item_lit) - 1)) + "]"
        assert isinstance(ast.literal_eval(node_lit), list)
        assert len(node_lit) > IMPORT_NODE_MAX_FILE_LEN
        try:
            write_file(imp_file, node_lit)
            node_file_info = app.import_file_info(imp_file)
            assert len(node_file_info) == 4
            assert not node_file_info[1]
            assert node_file_info[3]
        finally:
            if os.path.exists(imp_file):
                os.remove(imp_file)

    def test_import_file_info_too_much_nodes(self, restore_app_env):
        app = AppTest()

        name = 'info'
        imp_file = os.path.join(TESTS_FOLDER, f'node_{name}.txt')
        item_lit = "{'id': 'test'}, "
        node_lit = "[" + item_lit * (IMPORT_NODE_MAX_ITEMS + 1) + "]"
        node = ast.literal_eval(node_lit)
        assert isinstance(node, list)
        assert len(node) > IMPORT_NODE_MAX_ITEMS
        try:
            write_file(imp_file, node_lit)
            node_file_info = app.import_file_info(imp_file)
            assert len(node_file_info) == 4
            assert not node_file_info[1]
            assert node_file_info[3]
        finally:
            if os.path.exists(imp_file):
                os.remove(imp_file)

    def test_import_items(self, restore_app_env):
        app = AppTest()

        id1, id2 = 'test id to import', 'another item'
        node = [{'id': id1}, {'id': id2}]
        assert not app.current_node_items

        assert not app.import_items(node)
        assert len(app.current_node_items) == len(node)
        assert app.current_node_items == node

        assert app.import_items(node)       # check prevention of duplicates
        assert len(app.current_node_items) == len(node)
        assert app.current_node_items == node

    def test_import_node(self, restore_app_env):
        app = AppTest()

        id1, id2 = 'test id to import', 'another item'
        node = [{'id': id1}, {'id': id2}]
        assert not app.current_node_items

        assert not app.import_node('ori', node)
        assert len(app.current_node_items) == 1
        assert app.current_node_items[0]['id'] == 'ori'
        assert app.current_node_items[0]['node'][0]['id'] == id1

        assert not app.import_node('dup', node)
        assert len(app.current_node_items) == 2
        assert app.current_node_items[0]['id'] == 'dup'
        assert app.current_node_items[0]['node'][0]['id'] == id1

        assert app.import_node('dup', node)     # check prevention of duplicates
        assert len(app.current_node_items) == 2

    def test_item_by_id(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='0'), dict(id='3', node=[dict(id='69', node=[dict(id='999')])]), dict(id='6')]
        assert app.item_by_id('3') == app.root_node[1]

    def test_item_by_id_invalid(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='0'), dict(id='3', node=[dict(id='69', node=[dict(id='999')])]), dict(id='6')]
        assert app.item_by_id('x') == dict(id='x')

    def test_move_item_within_same_node(self, restore_app_env):
        app = AppTest()
        dragged_node = [dict(id='0'), dict(id='3', node=[dict(id='69', node=[dict(id='999')])]), dict(id='6')]
        assert app.move_item(dragged_node, '3')
        assert dragged_node == [dict(id='0'), dict(id='6'), dict(id='3', node=[dict(id='69', node=[dict(id='999')])])]

    def test_move_item_to_duplicate_sub_node(self, restore_app_env):
        app = AppTest()
        drop_node = [dict(id='0', node=[dict(id='999')])]
        app.root_node[:] = [dict(id='0'), dict(id='3', node=drop_node), dict(id='6')]
        assert not app.move_item(app.root_node, '0', dropped_path=[id_of_flow('enter', 'item', '3'), ])
        assert app.root_node == [dict(id='0'), dict(id='3', node=drop_node), dict(id='6')]

    def test_move_item_to_sub_node(self, restore_app_env):
        app = AppTest()
        drop_node = [dict(id='69', node=[dict(id='999')])]
        app.root_node[:] = [dict(id='0'), dict(id='3', node=drop_node), dict(id='6')]
        assert app.move_item(app.root_node, '0', dropped_path=[id_of_flow('enter', 'item', '3'), ])
        assert app.root_node == [dict(id='3', node=[dict(id='69', node=[dict(id='999')]), dict(id='0')]), dict(id='6')]

    def test_on_app_init_test_instance(self, restore_app_env):
        app = AppTest()
        app.on_app_init()
        assert app.current_node_items == []

    def test_on_app_init_mixin_instance(self, restore_app_env):
        app = AppTest()
        super(AppTest, app).on_app_init()
        assert app.current_node_items == []

    def test_on_app_start(self, restore_app_env):
        app = AppTest()
        app.on_app_start()
        assert app.current_node_items == []

    def test_on_app_state_key_save(self, restore_app_env):
        app = AppTest()
        app.root_node = [dict(id='0', sel=0), dict(id='3', sel=0.5, node=[
            dict(id='69', node=[dict(id='999', sel=1.0)])])]
        assert app.on_app_state_root_node_save(app.root_node) == [dict(id='0'), dict(id='3', node=[
            dict(id='69', node=[dict(id='999', sel=1.0)])])]

    def test_on_filter_toggle_set_sel(self, restore_app_env):
        app = AppTest()
        app.change_app_state('filter_selected', False)
        app.change_app_state('filter_unselected', False)

        app.on_filter_toggle('filter_selected', {})
        assert app.filter_selected
        assert not app.filter_unselected

        app.on_filter_toggle('filter_unselected', {})
        assert not app.filter_selected
        assert app.filter_unselected

        app.on_filter_toggle('filter_unselected', {})
        assert not app.filter_selected
        assert not app.filter_unselected

    def test_on_key_press_reset_flow(self, restore_app_env):
        app = AppTest()
        app.flow_path = [id_of_flow('enter', 'item', '3'), ]
        app.flow_id = id_of_flow('focus', 'item', '69')
        assert app.on_key_press('Shift', 'r')
        assert app.flow_path == []
        assert app.flow_id == id_of_flow('')

    def test_on_key_press_pass(self, restore_app_env):
        app = AppTest()
        assert not app.on_key_press('Shift', 'x')
        assert not app.on_key_press('', 'x')

        app.flow_id = id_of_flow('edit', 'item', '69')
        assert not app.on_key_press('', 'a')

    def test_on_key_press_focus_move(self, restore_app_env):
        app = AppTest()
        assert app.on_key_press('', 'up')
        assert app.on_key_press('', 'down')
        assert app.on_key_press('', 'pgup')
        assert app.on_key_press('', 'pgdown')
        assert app.on_key_press('', 'home')
        assert app.on_key_press('', 'end')

    def test_on_key_press_flow_change(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.current_node_items = app.root_node[0]['node']
        app.flow_path = [id_of_flow('enter', 'item', '3'), ]
        app.flow_id = id_of_flow('focus', 'item', '6')
        assert app.on_key_press('', ' ')
        assert app.on_key_press('', 'a')
        assert app.on_key_press('', '+')
        assert app.on_key_press('', 'e')
        assert app.on_key_press('', '-')
        assert app.on_key_press('', 'del')

        assert app.on_key_press('', 'enter')
        assert app.on_key_press('', 'escape')
        assert app.on_key_press('', 'left')
        app.current_node_items = app.root_node
        app.flow_id = id_of_flow('focus', 'item', '3')
        assert app.on_key_press('', 'right')

    def test_on_key_press_clipboard(self, restore_app_env):
        app = AppTest()
        assert not app.on_key_press('Ctrl', 'c')
        assert not app.on_key_press('Ctrl', 'v')
        assert not app.on_key_press('Ctrl', 'x')

    def test_on_key_press_clipboard_with_handler(self, restore_app_env):
        app = AppTest()
        app.on_clipboard_key_c = lambda: True
        assert app.on_key_press('Ctrl', 'c')
        app.on_clipboard_key_v = lambda: True
        assert app.on_key_press('Ctrl', 'v')
        app.on_clipboard_key_x = lambda: True
        assert app.on_key_press('Ctrl', 'x')

    def test_on_item_sel_change(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]

        event_kwargs = dict(set_sel_to=True)
        assert app.on_item_sel_change('3', event_kwargs)
        assert app.root_node[0].get('sel') == 1.0
        assert app.root_node[0]['node'][0].get('sel') == 1.0
        assert app.root_node[0]['node'][0]['node'][0].get('sel') == 1
        assert event_kwargs['flow_id'] == id_of_flow('focus', 'item', '3')

        app.current_node_items = app.root_node[0]['node'][0]['node']
        event_kwargs['set_sel_to'] = False
        assert app.on_item_sel_change('9', event_kwargs)
        assert app.root_node[0]['node'][0].get('sel') == 1.0
        assert event_kwargs['flow_id'] == id_of_flow('focus', 'item', '9')

    def test_on_node_extract_copy(self, restore_app_env):
        def copy_clipboard(cpy):
            """ clipboard copy receiver method """
            nonlocal copied
            copied = cpy

        app = AppTest()
        app.root_node[:] = [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[
                    dict(id='9u', sel=0), dict(id='9s', sel=1), dict(id='9', sel=0.6, node=[
                        dict(id='yz')
                    ])])])]
        root_copy = deepcopy(app.root_node)
        app.current_node_items = app.root_node[2]['node']   # we are displaying/in node '3'
        flow_id = id_of_flow('open', 'anything')
        app.flow_path = [id_of_flow('enter', 'item', '3'), flow_id, ]
        app.flow_id = flow_id
        copied = ""
        app.on_clipboard_key_c = copy_clipboard

        event_kwargs = dict(extract_type='copy')
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': 'yz'}]
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '9u'}, {'id': '9s', 'sel': 1}, {'id': '9', 'node': [{'id': 'yz'}]}]
        assert app.root_node == root_copy

        event_kwargs = dict(extract_type='copy_sel')
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert ast.literal_eval(copied) == []
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '9s', 'sel': 1}]
        assert app.on_node_extract('3', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '6s', 'sel': 1}, {'id': '6', 'node': [
            {'id': '9s', 'sel': 1}]}]
        assert app.root_node == root_copy

        event_kwargs = dict(extract_type='copy_unsel')
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': 'yz'}]
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '9u'}, {'id': '9', 'node': [{'id': 'yz'}]}]
        assert app.on_node_extract('3', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '6u'}, {'id': '6', 'node': [
            {'id': '9u'}, {'id': '9', 'node': [{'id': 'yz'}]}]}]
        assert app.root_node == root_copy

    def test_on_node_extract_cut(self, restore_app_env):
        def copy_clipboard(cpy):
            """ clipboard copy receiver method """
            nonlocal copied
            copied = cpy

        app = AppTest()
        app.root_node[:] = [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[
                    dict(id='9u', sel=0), dict(id='9s', sel=1), dict(id='9', sel=0.6, node=[
                        dict(id='yz')
                    ])])])]
        root_copy = deepcopy(app.root_node)
        app.current_node_items = app.root_node[2]['node']   # we are displaying/in node '3'
        flow_id = id_of_flow('open', 'anything')
        app.flow_path = [id_of_flow('enter', 'item', '3'), flow_id, ]
        app.flow_id = flow_id
        copied = ""
        app.on_clipboard_key_c = copy_clipboard

        event_kwargs = dict(extract_type='cut')
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': 'yz'}]
        assert app.root_node != root_copy
        assert app.root_node == [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[
                    dict(id='9u', sel=0), dict(id='9s', sel=1), dict(id='9', sel=0.6, node=[])])])]

        app.root_node[:] = deepcopy(root_copy)
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '9u'}, {'id': '9s', 'sel': 1}, {'id': '9', 'node': [{'id': 'yz'}]}]
        assert app.root_node != root_copy
        assert app.root_node == [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[])])]

        event_kwargs = dict(extract_type='cut_sel')
        app.root_node[:] = deepcopy(root_copy)
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert ast.literal_eval(copied) == []
        assert app.root_node == root_copy

        app.root_node[:] = deepcopy(root_copy)
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '9s', 'sel': 1}]
        assert app.root_node != root_copy

        app.root_node[:] = deepcopy(root_copy)
        assert app.on_node_extract('3', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '6s', 'sel': 1}, {'id': '6', 'node': [{'id': '9s', 'sel': 1}]}]
        assert app.root_node != root_copy
        assert app.root_node == [
            dict(id='3u'), {'id': '3s', 'sel': 1}, dict(id='3', sel=0.4, node=[
                dict(id='6u'), dict(id='6', node=[
                    dict(id='9u'), dict(id='9', node=[{'id': 'yz'}])])])]

        event_kwargs = dict(extract_type='cut_unsel')
        app.root_node[:] = deepcopy(root_copy)
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': 'yz'}]
        assert app.root_node != root_copy
        assert app.root_node == [{'id': '3u'}, {'id': '3s', 'sel': 1}, {'id': '3', 'sel': 0.4, 'node': [
            {'id': '6u', 'sel': 0}, {'id': '6s', 'sel': 1}, {'id': '6', 'sel': 0.5, 'node': [
                {'id': '9u', 'sel': 0}, {'id': '9s', 'sel': 1}, {'id': '9', 'sel': 0.6, 'node': []}]}]}]

        app.root_node[:] = deepcopy(root_copy)
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '9u'}, {'id': '9', 'node': [{'id': 'yz'}]}]
        assert app.root_node != root_copy
        assert app.root_node == [{'id': '3u'}, {'id': '3s', 'sel': 1}, {'id': '3', 'sel': 0.4, 'node': [
            {'id': '6u', 'sel': 0}, {'id': '6s', 'sel': 1}, {'id': '6', 'sel': 0.5, 'node': [
                {'id': '9s', 'sel': 1}]}]}]

        app.root_node[:] = deepcopy(root_copy)
        assert app.on_node_extract('3', event_kwargs)
        assert ast.literal_eval(copied) == [{'id': '6u'}, {'id': '6', 'node': [
            {'id': '9u'}, {'id': '9', 'node': [{'id': 'yz'}]}]}]
        assert app.root_node != root_copy
        assert app.root_node == [{'id': '3u'}, {'id': '3s', 'sel': 1}, {'id': '3', 'sel': 0.4, 'node': [
            {'id': '6s', 'sel': 1}, {'id': '6', 'node': [
                {'id': '9s', 'sel': 1}]}]}]

    def test_node_extract_export(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[
                    dict(id='9u', sel=0), dict(id='9s', sel=1), dict(id='9', sel=0.6, node=[
                        dict(id='yz')
                    ])])])]
        root_copy = deepcopy(app.root_node)
        cleaned_root_copy = deepcopy(root_copy)
        app.shrink_node_size(cleaned_root_copy)

        # app.current_node_items = app.root_node
        # app.flow_id = id_of_flow('open', 'anything')
        # app.flow_path = []

        event_kwargs = dict(export_path=TESTS_FOLDER, extract_type='export')

        file_name = os.path.join(TESTS_FOLDER, NODE_FILE_PREFIX + FLOW_PATH_ROOT_ID + NODE_FILE_EXT)
        try:
            assert app.on_node_extract('', event_kwargs)
            exported = read_file_text(file_name)
            assert ast.literal_eval(exported) == [{'id': '3u'}, {'id': '3s', 'sel': 1}, {'id': '3', 'node': [
                {'id': '6u'}, {'id': '6s', 'sel': 1}, {'id': '6', 'node': [
                    {'id': '9u'}, {'id': '9s', 'sel': 1}, {'id': '9', 'node': [{'id': 'yz'}]}]}]}]
            assert app.root_node == root_copy
            assert ast.literal_eval(exported) == cleaned_root_copy
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

        file_name = os.path.join(TESTS_FOLDER, NODE_FILE_PREFIX + '9' + NODE_FILE_EXT)
        try:
            assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
            exported = read_file_text(file_name)
            assert ast.literal_eval(exported) == [{'id': 'yz'}]
            assert app.root_node == root_copy
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

        file_name = os.path.join(TESTS_FOLDER, NODE_FILE_PREFIX + '6' + NODE_FILE_EXT)
        try:
            assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
            exported = read_file_text(file_name)
            assert ast.literal_eval(exported) == [{'id': '9u'}, {'id': '9s', 'sel': 1}, {'id': '9', 'node': [
                {'id': 'yz'}]}]
            assert app.root_node == root_copy
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

        file_name = os.path.join(TESTS_FOLDER, NODE_FILE_PREFIX + '3' + NODE_FILE_EXT)
        try:
            assert app.on_node_extract('3', event_kwargs)
            exported = read_file_text(file_name)
            assert ast.literal_eval(exported) == [{'id': '6u'}, {'id': '6s', 'sel': 1}, {'id': '6', 'node': [
                {'id': '9u'}, {'id': '9s', 'sel': 1}, {'id': '9', 'node': [
                    {'id': 'yz'}]}]}]
            assert app.root_node == root_copy
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)

    def test_on_node_extract_share(self, restore_app_env):
        def share(_flow_path, node=('default', )):
            """ share receiver method """
            nonlocal copied
            copied = node

        app = AppTest()
        app.root_node[:] = [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[
                    dict(id='9u', sel=0), dict(id='9s', sel=1), dict(id='9', sel=0.6, node=[
                        dict(id='yz')
                    ])])])]
        root_copy = deepcopy(app.root_node)
        app.current_node_items = app.root_node[2]['node']   # we are displaying/in node '3'
        flow_id = id_of_flow('open', 'anything')
        app.flow_path = [id_of_flow('enter', 'item', '3'), flow_id, ]
        app.flow_id = flow_id
        copied = ""
        app.share_node = share

        event_kwargs = dict(extract_type='share')
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert copied == [{'id': 'yz'}]
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert copied == [{'id': '9u'}, {'id': '9s', 'sel': 1}, {'id': '9', 'node': [{'id': 'yz'}]}]
        assert app.root_node == root_copy

        event_kwargs = dict(extract_type='share_sel')
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert copied == []
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert copied == [{'id': '9s', 'sel': 1}]
        assert app.on_node_extract('3', event_kwargs)
        assert copied == [{'id': '6s', 'sel': 1}, {'id': '6', 'node': [
            {'id': '9s', 'sel': 1}]}]
        assert app.root_node == root_copy

        event_kwargs = dict(extract_type='share_unsel')
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6' + FLOW_PATH_TEXT_SEP + '9', event_kwargs)
        assert copied == [{'id': 'yz'}]
        assert app.on_node_extract('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert copied == [{'id': '9u'}, {'id': '9', 'node': [{'id': 'yz'}]}]
        assert app.on_node_extract('3', event_kwargs)
        assert copied == [{'id': '6u'}, {'id': '6', 'node': [
            {'id': '9u'}, {'id': '9', 'node': [{'id': 'yz'}]}]}]
        assert app.root_node == root_copy

    def test_node_info(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[
                    dict(id='9u', sel=0), dict(id='9s', sel=1), dict(id='9', sel=0.6, node=[
                        dict(id='yz')
                    ])])])]

        flow_path = [id_of_flow('enter', 'item', '3'), id_of_flow('enter', 'item', '6'),
                     id_of_flow('enter', 'item', '9')]
        info = app.node_info(app.flow_path_node(flow_path))
        assert isinstance(info, dict)
        assert info

        assert info['names'] == ['yz']
        assert info['leaf_names'] == ['yz']
        assert info['selected_leaf_names'] == []
        assert info['unselected_leaf_names'] == ['yz']

        assert info['count'] == 1
        assert info['leaf_count'] == 1
        assert info['node_count'] == 0
        assert info['selected_leaf_count'] == 0
        assert info['unselected_leaf_count'] == 1

        flow_path = [id_of_flow('enter', 'item', '3'), id_of_flow('enter', 'item', '6')]
        info = app.node_info(app.flow_path_node(flow_path))
        assert isinstance(info, dict)
        assert info

        assert info['names'] == ['9u', '9s', '9', 'yz']
        assert info['leaf_names'] == ['9u', '9s', 'yz']
        assert info['selected_leaf_names'] == ['9s']
        assert info['unselected_leaf_names'] == ['9u', 'yz']

        assert info['count'] == 4
        assert info['leaf_count'] == 3
        assert info['node_count'] == 1
        assert info['selected_leaf_count'] == 1
        assert info['unselected_leaf_count'] == 2

        flow_path = [id_of_flow('enter', 'item', '3')]
        info = app.node_info(app.flow_path_node(flow_path))
        assert isinstance(info, dict)
        assert info

        assert info['names'] == ['6u', '6s', '6', '9u', '9s', '9', 'yz']
        assert info['leaf_names'] == ['6u', '6s', '9u', '9s', 'yz']
        assert info['selected_leaf_names'] == ['6s', '9s']
        assert info['unselected_leaf_names'] == ['6u', '9u', 'yz']

        assert info['count'] == 7
        assert info['leaf_count'] == 5
        assert info['node_count'] == 2
        assert info['selected_leaf_count'] == 2
        assert info['unselected_leaf_count'] == 3

        flow_path = []      # ROOT
        info = app.node_info(app.flow_path_node(flow_path))
        assert isinstance(info, dict)
        assert info

        assert info['names'] == ['3u', '3s', '3', '6u', '6s', '6', '9u', '9s', '9', 'yz']
        assert info['leaf_names'] == ['3u', '3s', '6u', '6s', '9u', '9s', 'yz']
        assert info['selected_leaf_names'] == ['3s', '6s', '9s']
        assert info['unselected_leaf_names'] == ['3u', '6u', '9u', 'yz']

        assert info['count'] == 10
        assert info['leaf_count'] == 7
        assert info['node_count'] == 3
        assert info['selected_leaf_count'] == 3
        assert info['unselected_leaf_count'] == 4

    def test_on_node_jump(self, restore_app_env):
        app = AppTest()
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.current_node_items = app.root_node[0]['node']
        flow_id = id_of_flow('open', 'jumper')
        app.flow_path = [id_of_flow('enter', 'item', '3'), flow_id, ]
        app.flow_id = flow_id
        event_kwargs = dict(set_sel_to=True)
        assert app.on_node_jump('3' + FLOW_PATH_TEXT_SEP + '6', event_kwargs)
        assert app.flow_path == [id_of_flow('enter', 'item', '3'), id_of_flow('enter', 'item', '6'), flow_id, ]

    def test_refresh_all(self, restore_app_env):
        app = AppTest()
        app.debug_level = 1
        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.flow_id = id_of_flow('focus', 'item', '3')
        app.refresh_all()
        assert app.flow_id == id_of_flow('')

        app.flow_id = id_of_flow('focus', 'item', '3')
        app.filtered_indexes = (0, )
        app.refresh_all()
        assert app.flow_id == id_of_flow('focus', 'item', '3')

    def test_shrink_node_size(self, restore_app_env):
        app = AppTest()
        app.root_node = [dict(id='0', sel=0), dict(id='3', sel=0.5, node=[
            dict(id='69', node=[dict(id='999', sel=1.0)])])]
        app.on_app_state_root_node_save(app.root_node)
        assert app.root_node == [dict(id='0'), dict(id='3', node=[
            dict(id='69', node=[dict(id='999', sel=1)])])]

    def test_sub_item_ids(self, restore_app_env):
        app = AppTest()
        assert app.sub_item_ids(item_ids=('3', )) == []

        app.root_node[:] = [dict(id='3', node=[dict(id='6', node=[dict(id='9')])])]
        app.current_node_items = app.root_node
        app.flow_path = []

        assert app.sub_item_ids(leaves_only=False) == ['3', '6', '9']
        assert app.sub_item_ids(item_ids=('3', ), leaves_only=False) == ['3', '6', '9']
        assert app.sub_item_ids(item_ids=('3', ), leaves_only=False, hide_sel_val=True) == ['3', '6', '9']
        assert app.sub_item_ids(item_ids=('3', ), leaves_only=False, hide_sel_val=False) == ['3', '6']
        assert app.sub_item_ids(node=app.root_node[0]['node'], item_ids=('6', ), leaves_only=False) == ['6', '9']
        assert app.sub_item_ids(node=app.root_node[0]['node'][0]['node'], item_ids=('9', ), leaves_only=False) == ['9']

        assert app.sub_item_ids() == ['9']
        assert app.sub_item_ids(recursive=False) == []
        assert app.sub_item_ids(item_ids=('abc', )) == []
        assert app.sub_item_ids(item_ids=('9', )) == []

        assert app.sub_item_ids(item_ids=('3', )) == ['9']
        assert app.sub_item_ids(item_ids=('3', ), hide_sel_val=True) == ['9']
        assert app.sub_item_ids(item_ids=('3', ), hide_sel_val=False) == []
        assert app.sub_item_ids(node=app.root_node[0]['node'], item_ids=('6', )) == ['9']
        assert app.sub_item_ids(node=app.root_node[0]['node'], item_ids=('6', ), hide_sel_val=True) == ['9']
        assert app.sub_item_ids(node=app.root_node[0]['node'], item_ids=('6', ), hide_sel_val=False) == []
        assert app.sub_item_ids(node=app.root_node[0]['node'][0]['node'], item_ids=('9', )) == ['9']

        app.root_node[:] = [
            dict(id='3u'), dict(id='3s', sel=1), dict(id='3', sel=0.4, node=[
                dict(id='6u', sel=0), dict(id='6s', sel=1), dict(id='6', sel=0.5, node=[
                    dict(id='9u', sel=0), dict(id='9s', sel=1), dict(id='9', sel=0.6, node=[
                        dict(id='yz')
                    ])])])]

        assert app.sub_item_ids(leaves_only=False) == ['3u', '3s', '3', '6u', '6s', '6', '9u', '9s', '9', 'yz']
        assert app.sub_item_ids(item_ids=('3', ), leaves_only=False) == ['3', '6u', '6s', '6', '9u', '9s', '9', 'yz']
        assert app.sub_item_ids(item_ids=('3', ), leaves_only=False, hide_sel_val=True) \
               == ['3', '6u', '6', '9u', '9', 'yz']
        assert app.sub_item_ids(item_ids=('3', ), leaves_only=False, hide_sel_val=False) == ['3', '6s', '6', '9s', '9']
        assert app.sub_item_ids(node=app.root_node[2]['node'], item_ids=('6', ), leaves_only=False
                                ) == ['6', '9u', '9s', '9', 'yz']
        assert app.sub_item_ids(node=app.root_node[2]['node'][2]['node'], item_ids=('9', ), leaves_only=False) \
               == ['9', 'yz']
        assert app.sub_item_ids(node=app.root_node[2]['node'][2]['node'], item_ids=('9', ), leaves_only=False,
                                hide_sel_val=True) == ['9', 'yz']
        assert app.sub_item_ids(node=app.root_node[2]['node'][2]['node'], item_ids=('9', ), leaves_only=False,
                                hide_sel_val=False) == ['9']

        assert app.sub_item_ids() == ['3u', '3s', '6u', '6s', '9u', '9s', 'yz']
        assert app.sub_item_ids(hide_sel_val=True) == ['3u', '6u', '9u', 'yz']
        assert app.sub_item_ids(hide_sel_val=False) == ['3s', '6s', '9s']
        assert app.sub_item_ids(item_ids=('3', )) == ['6u', '6s', '9u', '9s', 'yz']
        assert app.sub_item_ids(item_ids=('3', ), hide_sel_val=True) == ['6u', '9u', 'yz']
        assert app.sub_item_ids(item_ids=('3', ), hide_sel_val=False) == ['6s', '9s']
        assert app.sub_item_ids(node=app.root_node[2]['node'], item_ids=('6', )) == ['9u', '9s', 'yz']
        assert app.sub_item_ids(node=app.root_node[2]['node'], item_ids=('6', ), hide_sel_val=True) == ['9u', 'yz']
        assert app.sub_item_ids(node=app.root_node[2]['node'], item_ids=('6', ), hide_sel_val=False) == ['9s']
        assert app.sub_item_ids(node=app.root_node[2]['node'][2]['node'], item_ids=('9', )) == ['yz']
        assert app.sub_item_ids(node=app.root_node[2]['node'][2]['node'], item_ids=('9', ), hide_sel_val=True) == ['yz']
        assert app.sub_item_ids(node=app.root_node[2]['node'][2]['node'], item_ids=('9', ), hide_sel_val=False) == []

    def test_toggle_item_sel(self, restore_app_env):
        app = AppTest()
        tid = 'tst_id'
        app.current_node_items = [dict(id=tid)]

        assert 'sel' not in app.current_node_items[0]
        app.toggle_item_sel(0)
        assert 'sel' in app.current_node_items[0]
        assert app.current_node_items[0]['sel'] == 1

        app.toggle_item_sel(0)
        assert 'sel' not in app.current_node_items[0]
