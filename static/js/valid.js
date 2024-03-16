function isURLValid(url) {
    const pattern = /^(https?:\/\/)([\w-]+(\.[\w-]+)*|localhost)(:\d+)?(\/[\w.,@?^=%&:/~+#-]*)?$/i;
    return pattern.test(url);
}

function isEmailValid(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}

function isCardNumberValid(number) {
    return /^\d{16}$/.test(number);
}

function isCVCValid(cvc) {
    return /^\d{3,4}$/.test(cvc);
}

function isPinValid(pin) {
    return /^\d{4}$/.test(pin);
}

function isMonthValid(month) {
    return /^(0[1-9]|1[0-2])$/.test(month);
}

function isYearValid(year) {
    return /^(20[0-9][0-9]|2100)$/.test(year);
}

function isMasterPasswordValid(password) {
    return password.length >= 8 && password.length <= 128 &&
        /[0-9]/.test(password) &&
        /[a-z]/.test(password) &&
        /[A-Z]/.test(password) &&
        /[@&$!#?]/.test(password);
}
