document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('form_login').addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = e.target;

        const masterPassword = form.master_password.value;
        const email = form.email.value;

        try {
            const response = await fetch('/users/api?email=' + encodeURIComponent(email));
            if (!response.ok) {
                notifyError('Пользователь с данным адресом электронной почты не найден');
                return null;
            }

            const data = await response.json();

            const salt = hexToArrayBuffer(data.salt);
            const initVector = hexToArrayBuffer(data.init_vector);
            const encryptionKey = await generateKeyArgon2(masterPassword, salt);
            const authKey = await encryptAES(encryptionKey, masterPassword + salt, salt, initVector);

            form.auth_key.value = arrayBufferToHex(authKey);

            form.master_password.value = '0'.repeat(masterPassword.length);

            document.cookie = "key=" + encryptionKey + ";path=/;max-age=2600000";

            form.submit();
        } catch (error) {
            notifyError('Произошла ошибка при выполнении запроса');
            return null;
        }
    });
});