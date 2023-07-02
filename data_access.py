import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, TodoCategory, Todo
import consts


def get_session():
    """ セッション情報を返却 """
    db_path = os.path.join('sqlite:///', 'db', 'todo.db')
    engine = create_engine(db_path)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def find_user(input_name, input_password):
    """ 利用者検索 """
    session = get_session()
    user = session.query(User).filter_by(name=input_name, password=input_password).first()

    return user

def find_todo_all(u_id):
    """ 利用者IDをもとにTODOタスク一覧を取得する """
    session = get_session()
    todo_list = session.query(Todo).filter(Todo.user_id == u_id, Todo.status == consts.STATUS_INCOMPLETE).order_by(Todo.due_date.asc()).all()

    return todo_list

def update_todo_status(t_id):
    """ タスクのステータスを1（完了）に更新する """
    is_valid = True

    session = get_session()
    try:
        todo = session.get(Todo, t_id)
        todo.status = consts.STATUS_COMPLETE
        session.add(todo)
        session.commit()
    except:
        session.rollback()
        is_valid = False
    finally:
        session.close()

    return is_valid

def get_category_all():
    """ カテゴリ一覧取得 """
    session = get_session()
    return session.query(TodoCategory).all()

def insert_todo(todo):
    """ タスクの新規登録 """
    is_valid = True
    
    session = get_session()
    try:
        todo = Todo(
            title = todo["title"],
            content = todo["content"],
            memo = todo["memo"],
            due_date = todo["due_date"],
            category_id = todo["category_id"],
            user_id = todo["user_id"]
        )
        session.add(todo)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        is_valid = False
    finally:
        session.close()

    return is_valid

def get_todo(t_id):
    """ タスク情報取得 """
    session = get_session()
    return session.get(Todo, t_id)

def update_todo(todo_item):
    """ タスクの更新 """
    is_valid = True

    session = get_session()
    todo = session.get(Todo, todo_item["id"])
    if not todo:
        is_valid = False
    else:
        try:
            todo.title = todo_item["title"]
            todo.content = todo_item["content"]
            todo.memo = todo_item["memo"]
            todo.due_date = todo_item["due_date"]
            todo.category_id = todo_item["category_id"]

            session.add(todo)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            is_valid = False
        finally:
            session.close()

    return is_valid

def delete_task(t_id):
    """ タスクの削除 """
    is_valid = True

    session = get_session()
    try:
        session.query(Todo).filter_by(id=t_id).delete()
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        is_valid = False
    finally:
        session.close()
    
    return is_valid