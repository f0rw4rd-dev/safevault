document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('id_form_register').addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = e.target;

        const masterPassword = form.master_password.value;

        const salt = crypto.getRandomValues(new Uint8Array(16));
        const initVector = crypto.getRandomValues(new Uint8Array(16));
        const encryptionKey = await generateKeyArgon2(masterPassword, salt);
        const authKey = await encryptAES(encryptionKey, masterPassword + salt, initVector);

        form.auth_key.value = arrayBufferToHex(authKey);
        form.salt.value = arrayBufferToHex(salt)
        form.init_vector.value = arrayBufferToHex(initVector)

        form.master_password.value = '\u200B'.repeat(masterPassword.length);

        form.submit();
    });
});

setupPasswordHandlers('id_master_password', 'id_password_strength', 'id_generate_password');