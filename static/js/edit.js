"use strict";

/**
 * 更新ボタン押下時
 */
$(document).on("click", "#update", function(e) {
    // エラーメッセージの初期化
    $(".error-msg").text("");

    // 入力値検証
    if (!validateUpdate()) {
        e.preventDefault();
    }

    // 初期表示時の値
    let defaultVal = {
        category: $("#init_category").val().trim(),
        title: $("#init_title").val().trim(),
        content: $("#init_content").val().trim(),
        memo: $("#init_memo").val().trim(),
        due_date: $("#init_due_date").val().trim()
    }
    // 画面入力値
    let updateVal = {
        category: $("select[id=category").val().trim(),
        title: $("#title").val().trim(),
        content: $("#content").val().trim(),
        memo: $("#memo").val().trim(),
        due_date: $("#due_date").val().trim()
    };
    // 更新内容比較
    let updateFlg = false;
    for (let [key, val] of Object.entries(defaultVal)) {
        if (val !== updateVal[key]) {
            updateFlg = true;
            break;
        }
    }
    if (!updateFlg) {
        e.preventDefault();
        $("#error-message").text("値をどれか変更して更新ボタンを押してください。")
    }
});

/**
 * タスク更新入力チェック
 * 
 * @returns is_valid（true:正常/false：異常）
 */
function validateUpdate() {
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

