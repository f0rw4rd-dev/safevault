document.addEventListener('DOMContentLoaded', async (event) => {
    const email = getCookie('email');
    const encryptionKey = getCookie('encryptionKey');

    if (email === null || encryptionKey === null) {
        notifyError('Произошла непредвиденная ошибка');
        window.location.href = `${window.location.origin}/users/logout`;
        return null;
    }

    await decryptData(encryptionKey);

    setupEditAddressButtons(encryptionKey);
    setupCopyTextToClipboard();
    setupFormSubmit('id_form_add_address', encryptionKey);
    setupFormSubmit('id_form_edit_address', encryptionKey);
});

async function decryptData(encryptionKey) {
    const elements = document.querySelectorAll('.record_address');
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

function setupEditAddressButtons(encryptionKey) {
    document.querySelectorAll('.btn-edit-address').forEach(button => {
        button.addEventListener('click', async (e) => {
            const data = {
                title: e.currentTarget.getAttribute('data-title'),
                country: e.currentTarget.getAttribute('data-country'),
                region: e.currentTarget.getAttribute('data-region'),
                locality: e.currentTarget.getAttribute('data-locality'),
                street: e.currentTarget.getAttribute('data-street'),
                house: e.currentTarget.getAttribute('data-house'),
                zip_code: e.currentTarget.getAttribute('data-zip-code'),
                extra_data: e.currentTarget.getAttribute('data-extra-data'),
            };

            const form = document.getElementById('id_form_edit_address');

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
            country: form.country.value,
            region: form.region.value,
            locality: form.locality.value,
            street: form.street.value,
            house: form.house.value,
            zip_code: form.zip_code.value,
            extra_data: form.extra_data.value
        };

        // Check data
        if (formData.title.trim().length === 0
            || formData.country.trim().length === 0
            || formData.locality.trim().length === 0
            || formData.street.trim().length === 0
            || formData.house.trim().length === 0
            || formData.zip_code.trim().length === 0) {
            notifyError('Все обязательные поля должны быть заполнены');
            return null;
        }

        if (formData.title.trim().length > 48) {
            notifyError('Название заголовка не должно превышать 48 символов');
            return null;
        }

        if (formData.region.trim().length > 128) {
            notifyError('Название региона не должно превышать 128 символов');
            return null;
        }

        if (formData.locality.trim().length > 128) {
            notifyError('Название населенного пункта не должно превышать 128 символов');
            return null;
        }

        if (formData.street.trim().length > 128) {
            notifyError('Название улицы не должно превышать 128 символов');
            return null;
        }

        if (formData.house.trim().length > 16) {
            notifyError('Номер дома не должен превышать 16 символов');
            return null;
        }

        if (formData.zip_code.trim().length > 16) {
            notifyError('Индекс не должен превышать 16 символов');
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

async function updateAddressStatus(id, status) {
    const url = `${window.location.origin}/addresses/api/update/status/`;
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

async function deleteAddress(id) {
    const url = `${window.location.origin}/addresses/api/delete/`;
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