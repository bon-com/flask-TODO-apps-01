import business_logic
from datetime import datetime
import consts

def validate_login(form, errors):
    """ ログイン情報の入力チェックを行う """
    is_valid = True
    name = form.get("name")
    password = form.get("password")
    if not name or not password:
        errors.append("名前またはパスワードを入力してください。")
        is_valid = False

    return is_valid

def validate_input_todo(form):
    """ タスク登録または編集の入力チェックを行う """
    # カテゴリ 必須
    c_id = form.get("category")
    if not c_id:
        raise ValueError()

    # カテゴリ 範囲
    categories = business_logic.get_category_all()
    id_list = list(map(str, [category.id for category in categories]))
    if not c_id in id_list:
        raise ValueError()

    # タイトル 必須
    title = form.get("title")
    if not title:
        raise ValueError()

    # タスク内容 必須
    content = form.get("content")
    if not content:
        raise ValueError()

    # タスク期日 必須
    due_date = form.get("due_date")
    if not due_date:
        raise ValueError()

    # タスク期日 存在する日付 ※変換できない場合、ValueErrorが発生
    datetime.strptime(due_date, consts.DATE_FORMAT)
