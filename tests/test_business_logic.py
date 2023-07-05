import unittest
from datetime import datetime
import os
import sys
from unittest.mock import patch
# 上の階層のファイルをインポートする場合、以下を先に記載する必要あり
# 追加した上の階層のファイルを参照できるようになる
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import business_logic
from models import User, Todo, TodoCategory
import consts

class TestBusinessLogic(unittest.TestCase):
    """ ビジネスロジックのテストクラス """

    @patch("data_access.find_user")
    def test_find_user(self, mock_find_uer):
        """ find_userの取得確認 """
        # モック定義
        user = User(id=1, name="テスト", password="パス")
        mock_find_uer.return_value = user
        # 結果確認
        self.assertEqual(user, business_logic.find_user("テスト", "パス"))

    @patch("data_access.find_todo_all")
    def test_find_todo_all(self, mock_find_todo_all):
        """ find_todo_allの確認 """
        # モック定義
        todo1 = Todo(
            id=1, 
            title="ダミー1", 
            content="ダミータスク１",
            memo = "メモ1",
            status = 0,
            due_date = datetime(2023, 7, 10),
            category = TodoCategory(id=1, category_name="娯楽")
        )
        todo2 = Todo(
            id = 2, 
            title = "ダミー2", 
            content = "ダミータスク2",
            memo = "メモ2",
            status = 0,
            due_date = datetime(2023, 7, 11),
            category = TodoCategory(id=1, category_name="余暇")
        )
        mock_find_todo_all.return_value = [todo1, todo2]
        
        # 実行結果
        u_id = 1
        todos = business_logic.find_todo_all(u_id)

        # 想定結果
        todo_item1 = dict(
            id = 1,
            title = "ダミー1",
            content = "ダミータスク１",
            category = "娯楽",
            due_date = "2023-07-10",
            status = "未完了"
        )
        todo_item2 = dict(
            id = 2,
            title = "ダミー2",
            content = "ダミータスク2",
            category = "余暇",
            due_date = "2023-07-11",
            status = "未完了"
        )
        expected = [todo_item1, todo_item2]

        # 結果確認
        self.assertEqual(todos, expected)
        

    @patch("data_access.update_todo_status")
    def test_update_todo_status(self, mock_update_todo_status):
        """ update_todo_statusの確認 """
        # モック定義
        mock_update_todo_status.return_value = True
        # 実行
        t_id = 1
        result = business_logic.update_todo_status(t_id)
        # 結果確認
        self.assertTrue(result)
        # モック（mock）が特定の方法で1回だけ呼び出されたことを検証するためのメソッド
        # 指定した引数でモックが複数回呼び出されている場合
        # 引数が異なる場合、またはモックが全く呼び出されていない場合
        # このメソッドはAssertionErrorをスローする
        mock_update_todo_status.assert_called_once_with(t_id)

    @patch("data_access.get_category_all")
    def test_get_category_all(self, mock_get_category_all):
        """ get_category_allの確認 """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        # 結果確認
        self.assertEqual(categories, business_logic.get_category_all())

    @patch("data_access.insert_todo")
    def test_insert_todo(self, mock_insert_todo):
        """ insert_todoの確認 """
        # ダミーデータ定義
        dummy_uid = 1
        dummy_form = dict(
            title = "タイトル",
            content = "タスク内容",
            memo = "",
            due_date = "2023-07-03",
            category = 1 
        )
        # モック定義
        mock_insert_todo.return_value = False
        # 想定引数
        expected = dict(
            title = dummy_form.get("title"),
            content= dummy_form.get("content"),
            memo= dummy_form.get("memo", ""),
            due_date= datetime.strptime(dummy_form.get("due_date"), consts.DATE_FORMAT),
            user_id= dummy_uid,
            category_id= int(dummy_form.get("category"))
        )
        # 結果確認
        self.assertFalse(business_logic.insert_todo(dummy_form, dummy_uid))
        mock_insert_todo.assert_called_once_with(expected)

    @patch("data_access.get_todo")
    def test_get_todo(self, mock_get_todo):
        """ get_todoの確認 """
        # モック定義
        todo = Todo(
            id = 1,
            title = "タイトル",
            category = TodoCategory(id=1, category_name="娯楽"),
            content ="タスク内容",
            memo = "メモ",
            due_date = datetime(2023, 7, 7),
            status = 1
        )
        mock_get_todo.return_value = todo
        # 想定結果
        expected = dict(
            id = 1,
            title = "タイトル",
            category_id = "1",
            category = "娯楽",
            content ="タスク内容",
            memo = "メモ",
            due_date = "2023-07-07",
            status = "完了"
        )

        # 結果確認
        dummy_id = 1
        self.assertEqual(expected, business_logic.get_todo(dummy_id))
        mock_get_todo.assert_called_once_with(dummy_id)

    @patch("data_access.update_todo")
    def test_update_todo(self, mock_update_todo):
        """ update_todoの確認 """
        # ダミーデータ定義
        dummy_form = dict(
            id = 1,
            title = "タイトル",
            content ="タスク内容",
            memo = "メモ",
            due_date = "2023-07-07",
            category = "1"
        )
        # モック定義
        mock_update_todo.return_value = True
        # 想定引数
        expected = dict(
            id = 1,
            title = "タイトル",
            content ="タスク内容",
            memo = "メモ",
            due_date = datetime(2023, 7, 7),
            category_id = 1
        )
        # 想定結果
        self.assertTrue(business_logic.update_todo(dummy_form))
        mock_update_todo.assert_called_once_with(expected)

    @patch("data_access.delete_task")
    def test_delete_task(self, mock_delete_task):
        """ delete_taskの確認 """
        # モック定義
        mock_delete_task.return_value = False
        dummy_tid = 1
        # 結果確認
        self.assertFalse(business_logic.delete_task(dummy_tid))
        mock_delete_task.assert_called_once_with(dummy_tid)

if __name__ == '__main__':
    unittest.main()