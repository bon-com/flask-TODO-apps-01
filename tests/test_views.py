import unittest
from http import HTTPStatus
import os
import sys
# 上の階層のファイルをインポートする場合、以下を先に記載する必要あり
# 追加した上の階層のファイルを参照できるようになる
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from views import app, get_todo
from models import TodoCategory
from unittest.mock import patch

class TestViews(unittest.TestCase):
    """ ルーティングファイルのテストクラス """

    def setUp(self):
        """ セットアップ """
        # テスト用のクライアントを準備
        self.app = app.test_client()
        # flaskをテストモードで実行する
        # エラーが発生すると、即座に例外をスローする
        self.app.testing = True

    def test_index_route(self):
        """ indexメソッドのリダイレクト先確認 """
        # リクエスト
        res = self.app.get("/", follow_redirects=True)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertIn('利用者ログイン'.encode('utf-8'), res.data)
    
    def test_index_route_redirect(self):
        """ indexメソッドのリダイレクト確認 """
        # リクエスト
        res = self.app.get("/")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    def test_show_login_route(self):
        """ show_loginメソッドの遷移先確認 """
        # リクエスト
        res = self.app.get("/todo_apps")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData('利用者ログイン', res)

    def test_login_validate_error(self):
        """ 入力チェックエラー確認 """
        # POSTデータ作成
        post_data = dict(name="", password="")
        # リクエスト
        res = self.app.post("/todo_apps/login", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData('名前またはパスワードを入力してください。', res)
    
    def test_login_failure(self):
        """ ログイン失敗確認 """
        # POSTデータ作成
        post_data = dict(name="ありえないケース", password="ありえないケース")
        # リクエスト
        res = self.app.post("/todo_apps/login", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("名前またはパスワードが正しくありません。", res)

    def test_login_success(self):
        """ ログイン成功確認 """
        # POSTデータ
        post_data = dict(name="ヤマダ", password="1234")
        # リクエスト
        res = self.app.post("/todo_apps/login", data=post_data, follow_redirects=True)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("ヤマダ さんのタスク一覧", res)

    @patch("business_logic.find_todo_all")
    def test_top(self, mock_find_todo_all):
        """ TODOトップ画面表示確認 """
        # モック定義
        mock_find_todo_all.return_value = [{"id": 1, "title": "テスト用タスクタイトル", "content": "タスク内容", "category": "カテゴリ名","status": "未完了", "due_date": "2023-07-03"}]
        with self.app.session_transaction() as session:
            session["u_id"] = 5

        # リクエスト
        res = self.app.get("/todo_apps/top")
        # 結果確認
        self.assertEqual(res._status_code, HTTPStatus.OK)
        self.assertInResData("テスト用タスクタイトル", res)

    def test_logout(self):
        """ ログアウト確認 """
        # リクエスト
        res = self.app.get("/logout", follow_redirects=True)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("利用者ログイン", res)
        with self.app.session_transaction() as session:
            self.assertNotIn("u_id", session)

    def test_update_todo_done_failure(self):
        """ タスク完了更新の失敗確認 """
        # モック定義
        with self.app.session_transaction() as session:
            session["u_id"] = 1

        # ありえないタスクID
        t_id = 9999
        # リクエスト
        res = self.app.get(f"/todo_apps/top/task/{t_id}")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("更新に失敗しました。時間を空けて再度実行してください。", res)

    @patch("business_logic.update_todo_status") 
    def test_update_todo_done_success(self, mock_update_todo_status):
        """ タスク完了更新の成功確認 """
        # モック定義
        mock_update_todo_status.return_value = True
        # リクエスト
        t_id = 50
        res = self.app.get(f"/todo_apps/top/task/{t_id}", follow_redirects=False)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    @patch("business_logic.get_category_all")
    def test_show_create(self, mock_get_category_all):
        """ TODO登録画面の表示確認 """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        # リクエスト
        res = self.app.get("/todo_apps/create_input")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("娯楽", res)
        self.assertInResData("余暇", res)
        self.assertInResData("タスク登録", res)

    @patch("business_logic.get_category_all")
    def test_create_todo_input_error(self, mock_get_category_all):
        """ タスクの新規登録失敗確認（必須チェックエラー） """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        # POSTデータ
        post_data = dict(category="", title="", content="", due_date="")
        # リクエスト
        res = self.app.post("/todo_apps/create_todo", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("娯楽", res)
        self.assertInResData("余暇", res)
        self.assertInResData("カテゴリを選択してください。", res)
        self.assertInResData("タイトルを入力してください。", res)
        self.assertInResData("タスク内容を入力してください。", res)
        self.assertInResData("タスク期日を入力してください。", res)

    @patch("business_logic.get_category_all")
    @patch("validate_views.validate_input_todo")
    @patch("business_logic.insert_todo")
    def test_create_todo_db_error(self, mock_insert_todo, mock_validate_input_todo, mock_get_category_all):
        """ タスクの新規登録失敗確認（DB登録エラー） """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        mock_validate_input_todo.return_value = True
        mock_insert_todo.return_value = False
        with self.app.session_transaction() as session:
            session["u_id"] = 5

        # POSTデータ
        post_data = ""
        # リクエスト
        res = self.app.post("/todo_apps/create_todo", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("娯楽", res)
        self.assertInResData("余暇", res)
        self.assertInResData("タスクの登録に失敗しました。時間を空けて再度実行してください。", res)
        self.assertInResData("タスク登録", res)

    @patch("validate_views.validate_input_todo")
    @patch("business_logic.insert_todo")
    def test_create_todo_success(self, mock_insert_todo, mock_validate_input_todo):
        """ タスクの新規登録失敗確認（DB登録エラー） """
        # モック定義
        mock_validate_input_todo.return_value = True
        mock_insert_todo.return_value = True
        with self.app.session_transaction() as session:
            session["u_id"] = 5

        # POSTデータ
        post_data = ""
        # リクエスト
        res = self.app.post("/todo_apps/create_todo", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.FOUND)
 
    @patch("business_logic.get_todo")
    def test_show_detail(self, mock_get_todo):
        """ タスク詳細画面の表示確認 """
        # モック定義
        test_data = dict(
            id = "1",
            title = "テストタイトル",
            category_id = "1",
            category = "カテゴリ",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01",
            status = "未完了"
        )
        mock_get_todo.return_value = test_data
        # リクエスト
        t_id = 1
        res = self.app.get(f"/todo_apps/detail/{t_id}")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        for k, v in test_data.items():
            self.assertInResData(v, res)

    @patch("business_logic.get_category_all")
    @patch("business_logic.get_todo")
    def test_show_edit(self, mock_get_todo, mock_get_category_all):
        """ タスク編集画面の表示確認 """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        test_data = dict(
            id = "1",
            title = "テストタイトル",
            category_id = "1",
            category = "カテゴリ",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01",
        )
        mock_get_todo.return_value = test_data
        # リクエスト
        t_id = 1
        res = self.app.get(f"/todo_apps/edit/{t_id}")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("娯楽", res)
        self.assertInResData("余暇", res)
        for k, v in test_data.items():
            self.assertInResData(v, res)

    @patch("business_logic.get_category_all")
    def test_edit_todo_input_error(self, mock_get_category_all):
        """ タスクを編集する確認（入力エラー） """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        # POSTデータ
        post_data = dict(id="1", category="", title="", content="", due_date="")
        # リクエスト
        res = self.app.post("/todo_apps/edit/done", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("娯楽", res)
        self.assertInResData("余暇", res)
        self.assertInResData("カテゴリを選択してください。", res)
        self.assertInResData("タイトルを入力してください。", res)
        self.assertInResData("タスク内容を入力してください。", res)
        self.assertInResData("タスク期日を入力してください。", res)

    @patch("business_logic.update_todo")
    @patch("business_logic.get_category_all")
    def test_edit_todo_db_error(self, mock_get_category_all, mock_update_todo):
        """ タスクを編集する確認（DBエラー） """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        mock_update_todo.return_value = False
        # POSTデータ
        post_data = dict(
            id = "1",
            title = "テストタイトル",
            category = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01"
        )
        # リクエスト
        res = self.app.post("/todo_apps/edit/done", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("娯楽", res)
        self.assertInResData("余暇", res)
        self.assertInResData("タスクの更新に失敗しました。時間を空けて再度実行してください。", res)

    @patch("business_logic.update_todo")
    @patch("business_logic.get_category_all")
    def test_edit_todo_success(self, mock_get_category_all, mock_update_todo):
        """ タスクを編集する確認（DBエラー） """
        # モック定義
        categories = [
            TodoCategory(id=1, category_name="娯楽"),
            TodoCategory(id=2, category_name="余暇")
        ]
        mock_get_category_all.return_value = categories
        mock_update_todo.return_value = True
        # POSTデータ
        post_data = dict(
            id = "1",
            title = "テストタイトル",
            category = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01"
        )
        # リクエスト
        res = self.app.post("/todo_apps/edit/done", data=post_data)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.FOUND)

    @patch("business_logic.delete_task")
    def test_delete_todo_error(self, mock_delete_task):
        """ タスクの削除失敗 """
        # モック定義
        mock_delete_task.return_value = False
        # リクエスト
        t_id = 1
        res = self.app.get(f"/todo_apps/delete/{t_id}", follow_redirects=True)
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("DBを更新中にエラーが発生しました。時間を空けて、再度ログインからやりなおしてください。", res)

    @patch("business_logic.delete_task")
    def test_delete_todo_error(self, mock_delete_task):
        """ タスクの削除失敗 """
        # モック定義
        mock_delete_task.return_value = True
        # リクエスト
        t_id = 1
        res = self.app.get(f"/todo_apps/delete/{t_id}")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.FOUND) 

    def test_show_error_db_error(self):
        """ エラー画面表示確認（DBエラー） """
        # リクエスト
        res = self.app.get("/todo_apps/error?error_id=1")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("DBを更新中にエラーが発生しました。時間を空けて、再度ログインからやりなおしてください。", res)
        self.assertInResData("処理続行エラー", res)

    def test_show_error_other_error(self):
        """ エラー画面表示確認（DBエラー以外） """
        # リクエスト
        res = self.app.get("/todo_apps/error")
        # 結果確認
        self.assertEqual(res.status_code, HTTPStatus.OK)
        self.assertInResData("エラーが発生しました。時間を空けて、再度ログインからやりなおしてください。", res)
        self.assertInResData("処理続行エラー", res)

    def test_get_todo_1(self):
        """ タスク情報を返却確認（全て値あり） """
        form_item = dict(
            id = "1",
            title = "テストタイトル",
            category = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01"
        )
        actual = get_todo(form_item)
        expected = dict(
            id = "1",
            title = "テストタイトル",
            category_id = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01" 
        )
        self.assertEqual(actual, expected)

    def test_get_todo_2(self):
        """ タスク情報を返却確認（一部値なし） """
        form_item = dict(
            id = "",
            title = "テストタイトル",
            category = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01"
        )
        actual = get_todo(form_item)
        expected = dict(
            id = "",
            title = "テストタイトル",
            category_id = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01" 
        )
        self.assertEqual(actual, expected)
    
    def test_get_todo_3(self):
        """ タスク情報を返却確認（一部値なし） """
        form_item = dict(
            id = "1",
            title = "",
            category = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01"
        )
        actual = get_todo(form_item)
        expected = dict(
            id = "1",
            title = "",
            category_id = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01" 
        )
        self.assertEqual(actual, expected)
    
    def test_get_todo_4(self):
        """ タスク情報を返却確認（一部値なし） """
        form_item = dict(
            id = "1",
            title = "テストタイトル",
            category = "",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01"
        )
        actual = get_todo(form_item)
        expected = dict(
            id = "1",
            title = "テストタイトル",
            category_id = "",
            content = "タスク内容",
            memo = "メモ",
            due_date = "2023-07-01" 
        )
        self.assertEqual(actual, expected)
    
    def test_get_todo_5(self):
        """ タスク情報を返却確認（一部値なし） """
        form_item = dict(
            id = "1",
            title = "テストタイトル",
            category = "1",
            content = "",
            memo = "メモ",
            due_date = "2023-07-01"
        )
        actual = get_todo(form_item)
        expected = dict(
            id = "1",
            title = "テストタイトル",
            category_id = "1",
            content = "",
            memo = "メモ",
            due_date = "2023-07-01" 
        )
        self.assertEqual(actual, expected)

    def test_get_todo_6(self):
        """ タスク情報を返却確認（全て値あり） """
        form_item = dict(
            id = "1",
            title = "テストタイトル",
            category = "1",
            content = "タスク内容",
            memo = "",
            due_date = "2023-07-01"
        )
        actual = get_todo(form_item)
        expected = dict(
            id = "1",
            title = "テストタイトル",
            category_id = "1",
            content = "タスク内容",
            memo = "",
            due_date = "2023-07-01" 
        )
        self.assertEqual(actual, expected)

    def test_get_todo_7(self):
        """ タスク情報を返却確認（全て値あり） """
        form_item = dict(
            id = "1",
            title = "テストタイトル",
            category = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = ""
        )
        actual = get_todo(form_item)
        expected = dict(
            id = "1",
            title = "テストタイトル",
            category_id = "1",
            content = "タスク内容",
            memo = "メモ",
            due_date = "" 
        )
        self.assertEqual(actual, expected)

    def assertInResData(self, text, res):
        """ レスポンス内のHTMLに、指定したtext文字列は含まれるか確認 """
        self.assertIn(text.encode("utf-8"), res.data)


if __name__ == '__main__':
    unittest.main()
