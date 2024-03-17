document.addEventListener('DOMContentLoaded', () => {
    const rangeInput = document.getElementById('id_range');
    const rangeValueDisplay = document.getElementById('id_range_value');
    const passwordDisplay = document.getElementById('id_password');
    const useDigitsCheckbox = document.getElementById('id_use_digits');
    const useCapitalLettersCheckbox = document.getElementById('id_use_capital_letters');
    const useSymbolsCheckbox = document.getElementById('id_use_symbols');

    const updateRangeValue = () => {
        rangeValueDisplay.textContent = rangeInput.value;
    };
    updateRangeValue();

    rangeInput.addEventListener('input', () => {
        updateRangeValue();
        generateAndDisplayPassword();
    });

    useDigitsCheckbox.addEventListener('change', generateAndDisplayPassword);
    useCapitalLettersCheckbox.addEventListener('change', generateAndDisplayPassword);
    useSymbolsCheckbox.addEventListener('change', generateAndDisplayPassword);

    function generateAndDisplayPassword() {
        const length = parseInt(rangeInput.value, 10);
        const useUpperCase = useCapitalLettersCheckbox.checked;
        const useNumbers = useDigitsCheckbox.checked;
        const useSpecialChars = useSymbolsCheckbox.checked;
        const password = generatePassword(length, useUpperCase, useNumbers, useSpecialChars);
        passwordDisplay.value = password;

        updatePasswordStrength('id_password', 'id_password_strength');
    }

    generateAndDisplayPassword();
});
