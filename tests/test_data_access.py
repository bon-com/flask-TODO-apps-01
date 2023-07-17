import unittest
import os
import sys
from unittest.mock import patch
# 上の階層のファイルをインポートする場合、以下を先に記載する必要あり
# 追加した上の階層のファイルを参照できるようになる
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import data_access
from models import User

class TestDataAccess(unittest.TestCase):
    """ DBアクセスのテストクラス """
    @patch("data_access.get_session")
    def test_find_user(self, mock_get_session):
        """ find_userの確認 """
        # モック定義
        mock_session = mock_get_session.return_value
        mock_query = mock_session.query.return_value.filter_by.return_value
        expected = User(name="鈴木", password="12345")
        mock_query.first.return_value = expected
        # 実行結果
        res = data_access.find_user("鈴木", "12345")
        # 結果確認
        self.assertEqual(res.name, "鈴木")
        self.assertEqual(res.password, "12345")
        # モックが期待通り呼ばれたか確認
        mock_get_session.assert_called_once()
        mock_session.query.assert_called_with(User)
        mock_session.query.return_value.filter_by.assert_called_once_with(name="鈴木", password="12345")
        mock_query.first.assert_called_once()

if __name__ == '__main__':
    unittest.main()