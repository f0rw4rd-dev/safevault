function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(name, value, duration, secure) {
    let cookieString = `${encodeURIComponent(name)}=${encodeURIComponent(value)};path=/;max-age=${duration}`;

    if (secure) {
        cookieString += ';Secure';
    }

    document.cookie = cookieString;
}
