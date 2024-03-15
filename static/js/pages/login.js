document.addEventListener('DOMContentLoaded', (event) => {
    setupLoginFormSubmit();
});

function setupLoginFormSubmit() {
    document.getElementById('id_form_login').addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = e.target;

        const masterPassword = form.master_password.value;
        const email = form.email.value;

        const userEncryptionData = await getSaltAndInitVector(email);

        if (userEncryptionData === null) {
            notifyError('Произошла непредвиденная ошибка');
            return null;
        }

        const salt = userEncryptionData.salt;
        const initVector = userEncryptionData.initVector;
        const encryptionKey = await generateKeyArgon2(masterPassword, salt);
        const authKey = await encryptAES(encryptionKey, masterPassword + salt, initVector);

        form.auth_key.value = arrayBufferToHex(authKey);
        form.master_password.value = '\u200B'.repeat(masterPassword.length);

        setCookie('encryptionKey', arrayBufferToHex(encryptionKey), 2600000, false);
        setCookie('email', email, 2600000, false);

        form.submit();
    });
}