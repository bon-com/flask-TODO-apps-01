"use strict";

/**
 * 登録ボタン押下時
 */
$(document).on("click", "#regist", function(e) {
    // エラーメッセージの初期化
    $(".error-msg").text("");

    // 入力値検証
    if (!validateRegist()) {
        e.preventDefault();
    }
});

/**
 * タスク登録入力チェック
 * 
 * @returns is_valid（true:正常/false：異常）
 */
function validateRegist() {
    let is_valid = true;
    let errors = {};
    // カテゴリ 必須チェック
    let category = $("select[id=category").val().trim();
    if (!checkInputReq(category)) {
        is_valid = false;
        errors["category-error"] = "カテゴリを選択してください。";
    }
    // タイトル 必須チェック
    let title = $("#title").val();
    if (!checkInputReq(title)) {
        is_valid = false;
        errors["title-error"] = "タイトルを入力してください。";
    }
    // タスク内容 必須チェック
    let content = $("#content").val();
    if (!checkInputReq(content)) {
        is_valid = false;
        errors["content-error"] = "タスク内容を入力してください。";
    }
    // タスク期日 必須チェック
    let due_date = $("#due_date").val();
    if (!checkInputReq(due_date)) {
        is_valid = false;
        errors["due_date-error"] = "タスク期日を入力してください。";
    }

    // エラーメッセージ表示
    for (let key in errors) {
        $("#" + key).text(errors[key]);
    }

    return is_valid;

}

