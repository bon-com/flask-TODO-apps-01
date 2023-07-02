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

def validate_create_todo(form, error_dict):
    """ タスク新規登録の入力チェックを行う """
    is_valid = True
    # カテゴリ 必須
    c_id = form.get("category")
    if not c_id:
        error_dict["category"] = "カテゴリを選択してください。"
        is_valid = False
    else:
        # カテゴリ 範囲
        categories = business_logic.get_category_all()
        id_list = list(map(str, [category.id for category in categories]))
        if not c_id in id_list:
            error_dict["category"] = "不正なカテゴリが選択されています。"
            is_valid = False
    # タイトル 必須
    title = form.get("title")
    if not title:
        error_dict["title"] = "タイトルを入力してください。"
        is_valid = False
    # タスク内容 必須
    content = form.get("content")
    if not content:
        error_dict["content"] = "タスク内容を入力してください。"
        is_valid = False
    # タスク期日 必須
    due_date = form.get("due_date")
    if not due_date:
        error_dict["due_date"] = "タスク期日を入力してください。"
        is_valid = False
    else:
        # タスク期日 存在する日付
        try:
            datetime.strptime(due_date, consts.DATE_FORMAT)
        except ValueError:
            error_dict["due_date"] = "存在する日付を入力してください。"
            is_valid = False

    return is_valid
