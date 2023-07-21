"use strict";

/**
 * 削除ボタン押下時
 */
$(document).on("click", "#deleteTask", function(e) {
    e.preventDefault();

    // モーダル情報セット
    $("#confirmModalTitle").text("タスクの削除");
    $("#confirmModalContent").text("タスクを削除します。よろしいですか？");

    // モーダルの「はい」押下イベントを定義
    $("#confirmModalYes").on("click", function(e){
        window.location.href = $("#deleteTask").attr("href");
    });

    // モーダル表示
    let modal = new bootstrap.Modal($("#confirmModal"));
    modal.show();
});

