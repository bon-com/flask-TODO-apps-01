from flask import Flask, render_template, request, redirect, url_for, session
import business_logic
import validate_views
import consts

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
    if not validate_views.validate_login(request.form, errors):
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

@app.route("/todo_apps/top/task/<int:t_id>")
def update_todo_done(t_id):
    """ タスクを完了にする """
    is_valid = business_logic.update_todo_status(t_id)
    if not is_valid:
        errors = ["更新に失敗しました。時間を空けて再度実行してください。"]
        # タスク一覧を取得
        todos = business_logic.find_todo_all(session["u_id"])

        return render_template("top.html", todos=todos, errors=errors)
    else:
        return redirect(url_for("top"))

@app.route("/todo_apps/create_input")
def show_create():
    """ タスク新規登録画面を表示する """
    categories = business_logic.get_category_all()
    return render_template("create.html", categories=categories)

@app.route("/todo_apps/create_todo", methods=["POST"])
def create_todo():
    """ タスクを新規登録する """
    # 入力値検証
    error_dict = {}
    is_valid = validate_views.validate_input_todo(request.form, error_dict)
    if not is_valid:
        # 入力エラーの場合
        categories = business_logic.get_category_all()
        return render_template("create.html", categories=categories, error_dict=error_dict) 
    else:
        # タスク登録
        is_valid = business_logic.insert_todo(request.form, session["u_id"])
        if not is_valid:
            # DBエラーの場合
            categories = business_logic.get_category_all()
            error_msg = "タスクの登録に失敗しました。時間を空けて再度実行してください。"
            return render_template("create.html", categories=categories, error_msg=error_msg) 
        else:
            return redirect(url_for("top"))

@app.route("/todo_apps/detail/<int:t_id>")
def show_detail(t_id):
    """ タスク詳細画面を表示する """
    todo = business_logic.get_todo(t_id)
    return render_template("detail.html", todo=todo)

@app.route("/todo_apps/edit/<int:t_id>")
def show_edit(t_id):
    """ 編集画面を表示する """
    categories = business_logic.get_category_all()
    todo = business_logic.get_todo(t_id)
    return render_template("edit.html", categories=categories, todo=todo)

@app.route("/todo_apps/edit/done", methods=["POST"])
def edit_todo():
    """ タスクを編集する """
    # 入力値検証
    error_dict = {}
    is_valid = validate_views.validate_input_todo(request.form, error_dict)
    if not is_valid:
        # 入力エラーの場合
        categories = business_logic.get_category_all()
        todo = get_todo(request.form)
        return render_template("edit.html", categories=categories, error_dict=error_dict, todo=todo) 
    else:
        # タスク更新
        is_valid = business_logic.update_todo(request.form)
        if not is_valid:
            # DBエラーの場合
            categories = business_logic.get_category_all()
            error_msg = "タスクの更新に失敗しました。時間を空けて再度実行してください。"
            todo = get_todo(request.form)
            return render_template("edit.html", categories=categories, error_msg=error_msg, todo=todo) 
        else:
            return redirect(url_for("show_detail", t_id=request.form["id"]))

@app.route("/todo_apps/delete/<int:t_id>")
def delete_todo(t_id):
    """ タスクを削除する """
    is_valid = business_logic.delete_task(t_id)
    if not is_valid:
        # 削除エラーの場合
        return redirect(url_for("show_error", error_id=consts.DB_ERROR))
    else:
        return redirect(url_for('top'))

@app.route("/todo_apps/error")
def show_error():
    """ エラー画面を表示する """
    session.clear()
    error_id = request.args.get("error_id", "")
    if error_id == consts.DB_ERROR:
        # DBエラーの場合
        error_msg = "DBを更新中にエラーが発生しました。時間を空けて、再度ログインからやりなおしてください。"
    else:
        error_msg = "エラーが発生しました。時間を空けて、再度ログインからやりなおしてください。"
    
    return render_template("error.html", error_msg=error_msg)

def get_todo(form):
    """ タスク情報を返却する """
    todo = {
        "id": form.get("id"),
        "title": form.get("title", ""),
        "category_id": form.get("category", ""),
        "content": form.get("content", ""),
        "memo": form.get("memo", ""),
        "due_date": form.get("due_date", "")
    }

    return todo


if __name__ == '__main__':
    # 8080ポートで起動
    app.run(port=8080, debug=True)