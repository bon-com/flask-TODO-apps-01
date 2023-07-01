from flask import Flask, render_template, request, redirect, url_for, session
import business_logic
from datetime import datetime
app = Flask(__name__)
app.secret_key = "yiYKQmFC6MTVKs5THpKkD"

@app.route("/")
def index():
    return redirect(url_for("show_login"))

@app.route("/todo_apps")
def show_login():
    """ ログイン画面表示 """
    return render_template("login.html")

@app.route("/todo_apps/login", methods=["POST"])
def login():
    """ ログイン処理 """
    # 入力値検証
    errors = []
    if not validate_login(request.form, errors):
        return render_template("login.html", errors=errors)
    
    # ログイン確認
    name = request.form["name"]
    password = request.form["password"]
    user = business_logic.find_user(name, password)
    if user:
        # ログイン成功
        session["name"] = user.name
        session["u_id"] = user.id
        return redirect(url_for("top"))
    else:
        # ログイン失敗
        errors.append("名前またはパスワードが正しくありません。")
        return render_template("login.html", errors=errors)

@app.route("/todo_apps/top")
def top():
    """ TODOタスク一覧画面表示 """
    # タスク一覧を取得
    todos = business_logic.find_todo_all(session["u_id"])

    return render_template("top.html", todos=todos)

@app.route("/logout")
def logout():
    """ ログアウト """
    session.clear()
    return redirect(url_for("show_login"))

@app.route("/todo_apps/top/task/<t_id>")
def update_todo_done(t_id):
    """ タスクを完了にする """
    is_valid = business_logic.update_todo_status(int(t_id))
    if not is_valid:
        errors = ["更新に失敗しました。時間を空けて再度実行してください。"]
        # タスク一覧を取得
        todos = business_logic.find_todo_all(session["u_id"])

        return render_template("top.html", todos=todos, errors=errors)
    else:
        return redirect(url_for("top"))

@app.route("/todo_apps/create_input")
def show_create():
    categories = business_logic.get_category_all()
    return render_template("create.html", categories=categories)

@app.route("/todo_apps/create_todo", methods=["POST"])
def create_todo():
    """ タスクを新規登録する """
    # 入力値検証
    error_dict = {}
    is_valid = validate_create_todo(request.form, error_dict)
    if not is_valid:
        # 入力エラーの場合
        categories = business_logic.get_category_all()
        return render_template("create.html", categories=categories, error_dict=error_dict) 
    else:
        # タスク登録
        is_valid = business_logic.insert_todo(request.form, session["u_id"])
        if not is_valid:
            # 入力エラーの場合
            categories = business_logic.get_category_all()
            error_msg = "タスクの登録に失敗しました。時間を空けて再度実行してください。"
            return render_template("create.html", categories=categories, error_msg=error_msg) 
        else:
            return redirect(url_for("top"))

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
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            error_dict["due_date"] = "存在する日付を入力してください。"
            is_valid = False

    return is_valid



if __name__ == '__main__':
    # 8080ポートで起動
    app.run(port=8080, debug=True)