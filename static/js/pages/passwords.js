document.addEventListener('DOMContentLoaded', async (event) => {
    const email = getCookie('email');
    const encryptionKey = getCookie('encryptionKey');

    if (email === null || encryptionKey === null) {
        notifyError('Произошла непредвиденная ошибка');
        window.location.href = `${window.location.origin}/users/logout`;
        return null;
    }

    await decryptData(encryptionKey);

    setupEditPasswordButtons(encryptionKey);
    setupCopyTextToClipboard();
    setupPasswordGeneratorAndStrengthEstimation('id_add_password', 'id_add_password_strength', 'id_add_generate_password');
    setupPasswordGeneratorAndStrengthEstimation('id_edit_password', 'id_edit_password_strength', 'id_edit_generate_password');
    setupFormSubmit('id_form_add_password', encryptionKey);
    setupFormSubmit('id_form_edit_password', encryptionKey);
});

async function decryptData(encryptionKey) {
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
}

function setupEditPasswordButtons(encryptionKey) {
    document.querySelectorAll('.btn-edit-password').forEach(button => {
        button.addEventListener('click', async (e) => {
            const data = {
                title: e.currentTarget.getAttribute('data-title'),
                website: e.currentTarget.getAttribute('data-website'),
                login: e.currentTarget.getAttribute('data-login'),
                email: e.currentTarget.getAttribute('data-email'),
                password: e.currentTarget.getAttribute('data-password'),
                extra_data: e.currentTarget.getAttribute('data-extra-data')
            };

            const form = document.getElementById('id_form_edit_password');

            const favorite = e.currentTarget.getAttribute('data-status') === '1';
            const initVector = e.currentTarget.getAttribute('data-init-vector');
            const id = e.currentTarget.getAttribute('data-id');

            for (const key of Object.keys(data)) {
                if (form.elements[key]) {
                    form.elements[key].value = await decryptAES(hexToArrayBuffer(encryptionKey), hexToArrayBuffer(data[key]), hexToArrayBuffer(initVector));
                }
            }

            form.favorite.checked = favorite;
            form.init_vector.value = initVector;
            form.id.value = id;
        });
    });
}

function setupFormSubmit(formId, encryptionKey) {
    document.getElementById(formId).addEventListener('submit', async function (e) {
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

        // Check data
        if (formData.title.trim().length === 0 || formData.login.trim().length === 0 || formData.password.trim().length === 0) {
            notifyError('Все обязательные поля должны быть заполнены');
            return null;
        }

        if (formData.email.trim().length > 0 && !isEmailValid(formData.email)) {
            notifyError('Некорректный формат почты');
            return null;
        }

        if (formData.website.trim().length > 0 && !isURLValid(formData.website)) {
            notifyError('Некорректный формат адреса веб-сайта, он должен быть полным');
            return null;
        }

        if (formData.title.trim().length > 48) {
            notifyError('Название заголовка не должно превышать 48 символов');
            return null;
        }

        if (formData.title.trim().length > 256) {
            notifyError('Адрес веб-сайта не должен превышать 256 символов');
            return null;
        }

        if (formData.login.trim().length > 128) {
            notifyError('Логин не должен превышать 128 символов');
            return null;
        }

        if (formData.password.trim().length > 128) {
            notifyError('Пароль не должен превышать 128 символов');
            return null;
        }

        if (formData.extra_data.trim().length > 4096) {
            notifyError('Дополнительные данные не должны превышать 4096 символов');
            return null;
        }

        // Encrypt all data
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
}