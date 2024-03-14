function notifySuccess(text, redirectUrl = null) {
    Toastify({
        text: text,
        duration: 1500,
        newWindow: true,
        // close: true,
        gravity: "top",
        position: "right",
        style: {
            background: "#198754",
        },
        callback: function () {
            if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        }
    }).showToast();
}

function notifyError(text, redirectUrl = null) {
    Toastify({
        text: text,
        duration: 1500,
        newWindow: true,
        // close: true,
        gravity: "top",
        position: "right",
        style: {
            background: "#dc3545",
        },
        callback: function () {
            if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        }
    }).showToast();
}

function notifyWarning(text, redirectUrl = null) {
    Toastify({
        text: text,
        duration: 1500,
        newWindow: true,
        // close: true,
        gravity: "top",
        position: "right",
        style: {
            background: "#ffc107",
        },
        callback: function () {
            if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        }
    }).showToast();
}