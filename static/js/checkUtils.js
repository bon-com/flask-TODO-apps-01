"use strict";

/**
 * 必須チェック
 * 
 * @param val チェック対象の値
 * @returns is_valid（true:正常/false:異常）
 */
function checkInputReq(val) {
    let is_valid = true;
    if (val === null || val === "") {
        is_valid = false;
    }

    return is_valid;
}