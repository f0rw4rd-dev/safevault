function setupPasswordHandlers(passwordId, passwordStrengthId, generatePasswordId) {
    document.getElementById(generatePasswordId).onclick = function () {
        const newPassword = generatePassword(16, true, true, true);
        const inputElement = document.getElementById(passwordId);
        inputElement.value = newPassword;
        inputElement.type = "text";
        updatePasswordStrength(passwordId, passwordStrengthId);
    };

    document.getElementById(passwordId).addEventListener('input', function () {
        this.value = this.value.replace(/[^a-zA-Z0-9@&$!#?]/g, '');
        updatePasswordStrength(passwordId, passwordStrengthId);
    });
}

function updatePasswordStrength(passwordId, passwordStrengthId) {
    const password = document.getElementById(passwordId);
    const passwordStrength = document.getElementById(passwordStrengthId);

    if (password.value === '') {
        passwordStrength.textContent = '';
        passwordStrength.classList.remove('text-danger', 'text-warning', 'text-success', 'text-primary');
        return;
    }

    const strength = evaluatePasswordStrength(password.value);
    passwordStrength.classList.remove('text-danger', 'text-warning', 'text-success', 'text-primary');

    switch (strength) {
        case 0:
            passwordStrength.textContent = 'Слабый';
            passwordStrength.classList.add('text-danger');
            break;
        case 1:
            passwordStrength.textContent = 'Средний';
            passwordStrength.classList.add('text-warning');
            break;
        case 2:
            passwordStrength.textContent = 'Сильный';
            passwordStrength.classList.add('text-success');
            break;
        case 3:
            passwordStrength.textContent = 'Очень сильный';
            passwordStrength.classList.add('text-primary');
            break;
    }
}