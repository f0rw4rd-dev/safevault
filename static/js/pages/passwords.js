document.addEventListener('DOMContentLoaded', async (event) => {
    const email = getCookie('email');
    const encryptionKey = getCookie('encryptionKey');

    if (email === null || encryptionKey === null) {
        notifyError('Произошла непредвиденная ошибка');
        window.location.href = `${window.location.origin}/users/logout`;
        return null;
    }

    // Decrypt all data
    const elements = document.querySelectorAll('.record_password');
    const decryptionPromises = [];

    for (const element of elements) {
        const promise = (async () => {
            const data = hexToArrayBuffer(element.tagName.toLowerCase() === 'input' ? element.value : element.textContent);
            const decryptedData = await decryptAES(hexToArrayBuffer(encryptionKey), data, hexToArrayBuffer(element.getAttribute('data-init-vector')));

            return {element, decryptedData};
        })();
        decryptionPromises.push(promise);
    }

    const results = await Promise.all(decryptionPromises);

    for (const {element, decryptedData} of results) {
        switch (element.tagName.toLowerCase()) {
            case 'h5':
            case 'a':
                element.textContent = decryptedData;
                if (element.tagName.toLowerCase() === 'a') {
                    element.href = decryptedData;
                }
                break;
            case 'input':
                element.value = decryptedData;
                break;
        }
    }

    setupCopyTextToClipboard();

    document.getElementById('id_form_add_password').addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = e.target;

        const initVector = crypto.getRandomValues(new Uint8Array(16));

        const formData = {
            title: form.title.value,
            website: form.website.value,
            login: form.login.value,
            email: form.email.value,
            password: form.password.value,
            extra_data: form.extra_data.value
        };

        const encryptedData = await Promise.all(
            Object.entries(formData).map(async ([key, value]) => ({
                [key]: arrayBufferToHex(await encryptAES(hexToArrayBuffer(encryptionKey), value, initVector))
            }))
        );

        encryptedData.forEach(data => {
            const [key, value] = Object.entries(data)[0];
            form[key].value = value;
        });

        form.init_vector.value = arrayBufferToHex(initVector);

        form.submit()
    });
});

setupPasswordHandlers('id_add_password', 'id_add_password_strength', 'id_add_generate_password');
// setupPasswordHandlers('id_edit_password', 'id_edit_password_strength', 'id_edit_generate_password');