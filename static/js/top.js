"use strict";

/**
 * ログアウトボタン押下時
 */
$(document).on("click", "#logout", function(e) {
    e.preventDefault();

    // モーダル情報セット
    $("#confirmModalTitle").text("確認");
    $("#confirmModalContent").text("ログアウトしてもよろしいですか？");

    // モーダルの「はい」押下イベントを定義
    $("#confirmModalYes").on("click", function(e){
        window.location.href = $("#logout").attr("href");
    });

    // モーダル表示
    let modal = new bootstrap.Modal($("#confirmModal"));
    modal.show();
});

