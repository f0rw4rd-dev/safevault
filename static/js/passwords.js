function generatePassword(length, useUpperCase, useNumbers, useSpecialChars) {
    const lowerCaseLetters = 'abcdefghijklmnopqrstuvwxyz';
    const upperCaseLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const numbers = '0123456789';
    const specialChars = '(@&$!#?)';

    let allChars = lowerCaseLetters;
    let password = lowerCaseLetters.charAt(Math.floor(Math.random() * lowerCaseLetters.length));

    if (useUpperCase) {
        allChars += upperCaseLetters;
        password += upperCaseLetters.charAt(Math.floor(Math.random() * upperCaseLetters.length));
    }

    if (useNumbers) {
        allChars += numbers;
        password += numbers.charAt(Math.floor(Math.random() * numbers.length));
    }

    if (useSpecialChars) {
        allChars += specialChars;
        password += specialChars.charAt(Math.floor(Math.random() * specialChars.length));
    }

    for (let i = password.length; i < length; i++) {
        password += allChars.charAt(Math.floor(Math.random() * allChars.length));
    }

    password = password.split('').sort(() => 0.5 - Math.random()).join('');

    return password;
}

function evaluatePasswordStrength(password) {
    let score = 0;

    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (password.length >= 16) score++;

    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[(@&$!#?)]/.test(password)) score++;

    if (score <= 3) return 0;
    if (score <= 5) return 1;
    if (score <= 6) return 2;

    return 3;
}