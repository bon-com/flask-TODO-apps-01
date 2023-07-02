import data_access
import consts
from datetime import datetime

def find_user(name, password):
  """ userを取得する """
  # 名前とパスワードからuserオブジェクトを取得
  return data_access.find_user(name, password)

def find_todo_all(u_id):
    """ タスク一覧を取得する """
    # userに紐づくタスク一覧の取得
    todo_list = data_access.find_todo_all(u_id)
    todos = []
    for todo in todo_list:
        # 画面表示用データに整形
        todo_item = {
            "id": todo.id,
            "title": todo.title,
            "category": todo.category.category_name,
            "content": todo.content,
            "due_date": f"{todo.due_date:%Y-%m-%d}",
            "status": "未完了" if todo.status == consts.STATUS_INCOMPLETE else "完了"
        }
        todos.append(todo_item)

    return todos

def update_todo_status(t_id):
    """ タスクを完了にする """
    return data_access.update_todo_status(t_id)

def get_category_all():
    """ カテゴリ一覧取得 """
    return data_access.get_category_all()

def insert_todo(form, u_id):
    """ タスクの新規登録 """
    todo = {
        "title": form.get("title"),
        "content": form.get("content"),
        "memo": form.get("memo", ""),
        "due_date": datetime.strptime(form.get("due_date"), consts.DATE_FORMAT),
        "user_id": u_id,
        "category_id": int(form.get("category"))
    }

    return data_access.insert_todo(todo)

def get_todo(t_id):
    """ タスク情報取得 """
    todo = data_access.get_todo(t_id)
    todo_item = {
        "id": todo.id,
        "title": todo.title,
        "category_id": str(todo.category.id),
        "category": todo.category.category_name,
        "content": todo.content,
        "memo": todo.memo,
        "due_date": f"{todo.due_date:%Y-%m-%d}",
        "status": "未完了" if todo.status == consts.STATUS_INCOMPLETE else "完了"
    }

    return todo_item

def update_todo(form):
    """ タスクの更新 """    
    todo_item = {
        "id": form.get("id"),
        "title": form.get("title"),
        "content": form.get("content"),
        "memo": form.get("memo", ""),
        "due_date": datetime.strptime(form.get("due_date"), consts.DATE_FORMAT),
        "category_id": int(form.get("category"))
    }

    return data_access.update_todo(todo_item)

def delete_task(t_id):
    """ タスクの削除 """
    return data_access.delete_task(t_id)
