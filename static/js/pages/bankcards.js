document.addEventListener('DOMContentLoaded', async (event) => {
    const email = getCookie('email');
    const encryptionKey = getCookie('encryptionKey');

    if (email === null || encryptionKey === null) {
        notifyError('Произошла непредвиденная ошибка');
        window.location.href = `${window.location.origin}/users/logout`;
        return null;
    }

    await decryptData(encryptionKey);

    setupEditBankcardButtons(encryptionKey);
    setupCopyTextToClipboard();
    setupFormSubmit('id_form_add_bankcard', encryptionKey);
    setupFormSubmit('id_form_edit_bankcard', encryptionKey);
});

async function decryptData(encryptionKey) {
    const elements = document.querySelectorAll('.record_bankcard');
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

function setupEditBankcardButtons(encryptionKey) {
    document.querySelectorAll('.btn-edit-bankcard').forEach(button => {
        button.addEventListener('click', async (e) => {
            const data = {
                title: e.currentTarget.getAttribute('data-title'),
                card_number: e.currentTarget.getAttribute('data-card-number'),
                card_expiration_month: e.currentTarget.getAttribute('data-card-expiration-month'),
                card_expiration_year: e.currentTarget.getAttribute('data-card-expiration-year'),
                card_security_code: e.currentTarget.getAttribute('data-card-security-code'),
                card_pin: e.currentTarget.getAttribute('data-card-pin'),
                cardholder_name: e.currentTarget.getAttribute('data-cardholder-name'),
                extra_data: e.currentTarget.getAttribute('data-extra-data'),
            };

            const form = document.getElementById('id_form_edit_bankcard');

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
            card_number: form.card_number.value,
            card_expiration_month: form.card_expiration_month.value,
            card_expiration_year: form.card_expiration_year.value,
            card_security_code: form.card_security_code.value,
            card_pin: form.card_pin.value,
            cardholder_name: form.cardholder_name.value,
            extra_data: form.extra_data.value
        };

        // Check data
        if (formData.title.trim().length === 0
            || formData.card_number.trim().length === 0
            || formData.card_expiration_month.trim().length === 0
            || formData.card_expiration_year.trim().length === 0
            || formData.card_security_code.trim().length === 0
            || formData.card_pin.trim().length === 0) {
            notifyError('Все обязательные поля должны быть заполнены');
            return null;
        }

        if (formData.card_number.trim().length > 0 && !isCardNumberValid(formData.card_number)) {
            notifyError('Некорректный номер банковской карты');
            return null;
        }

        if (formData.card_expiration_month.trim().length > 0 && !isMonthValid(formData.card_expiration_month)) {
            notifyError('Некорректный месяц истечения срока действия карты');
            return null;
        }

        if (formData.card_expiration_year.trim().length > 0 && !isYearValid(formData.card_expiration_year)) {
            notifyError('Некорректный год истечения срока действия карты');
            return null;
        }

        if (formData.card_security_code.trim().length > 0 && !isCVCValid(formData.card_security_code)) {
            notifyError('Некорректный CVC/CVV код');
            return null;
        }

        if (formData.card_pin.trim().length > 0 && !isPinValid(formData.card_pin)) {
            notifyError('Некорректный пин-код карты');
            return null;
        }

        if (formData.title.trim().length > 48) {
            notifyError('Название заголовка не должно превышать 48 символов');
            return null;
        }

        if (formData.cardholder_name.trim().length > 128) {
            notifyError('Имя владельца карты не должно превышать 128 символов');
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

async function updateBankcardStatus(id, status) {
    const url = `${window.location.origin}/bankcards/api/update/status/`;
    const data = {id: id, status: status};
    const csrftoken = getCookie('csrftoken');
    const errorMessage = 'Не удалось выполнить действие';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('');
        }

        const jsonResponse = await response.json();

        if (jsonResponse.status === 'ok') {
            notifySuccess('Запись успешно обновлена', window.location.href);
        } else {
            notifyError(errorMessage);
        }
    } catch (error) {
        notifyError(errorMessage);
    }
}

async function deleteBankcard(id) {
    const url = `${window.location.origin}/bankcards/api/delete/`;
    const data = {id: id};
    const csrftoken = getCookie('csrftoken');
    const errorMessage = 'Не удалось выполнить действие';

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('');
        }

        const jsonResponse = await response.json();

        if (jsonResponse.status === 'ok') {
            notifySuccess('Запись успешно удалена', window.location.href);
        } else {
            notifyError(errorMessage);
        }
    } catch (error) {
        notifyError(errorMessage);
    }
}