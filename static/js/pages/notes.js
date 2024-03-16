document.addEventListener('DOMContentLoaded', async (event) => {
    const email = getCookie('email');
    const encryptionKey = getCookie('encryptionKey');

    if (email === null || encryptionKey === null) {
        notifyError('Произошла непредвиденная ошибка');
        window.location.href = `${window.location.origin}/users/logout`;
        return null;
    }

    await decryptData(encryptionKey);

    setupEditNoteButtons(encryptionKey);
    setupCopyTextToClipboard();
    setupFormSubmit('id_form_add_note', encryptionKey);
    setupFormSubmit('id_form_edit_note', encryptionKey);
});

async function decryptData(encryptionKey) {
    const elements = document.querySelectorAll('.record_note');
    const decryptionPromises = [];

    for (const element of elements) {
        const promise = (async () => {
            const encryptedData = element.tagName.toLowerCase() === 'textarea' ? element.value.trim() : element.textContent.trim();
            const dataBuffer = hexToArrayBuffer(encryptedData);
            const decryptedData = await decryptAES(hexToArrayBuffer(encryptionKey), dataBuffer, hexToArrayBuffer(element.getAttribute('data-init-vector')));
            return {element, decryptedData};
        })();
        decryptionPromises.push(promise);
    }

    const results = await Promise.all(decryptionPromises);

    for (const {element, decryptedData} of results) {
        if (element.tagName.toLowerCase() === 'textarea' || element.tagName.toLowerCase() === 'input') {
            element.value = decryptedData;
        } else {
            element.textContent = decryptedData;
        }
    }
}

function setupEditNoteButtons(encryptionKey) {
    document.querySelectorAll('.btn-edit-note').forEach(button => {
        button.addEventListener('click', async (e) => {
            const data = {
                title: e.currentTarget.getAttribute('data-title'),
                data: e.currentTarget.getAttribute('data-data'),
            };

            const form = document.getElementById('id_form_edit_note');

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
            data: form.data.value
        };

        // Check data
        if (formData.title.trim().length === 0
            || formData.data.trim().length === 0) {
            notifyError('Все обязательные поля должны быть заполнены');
            return null;
        }

        if (formData.title.trim().length > 48) {
            notifyError('Название заголовка не должно превышать 48 символов');
            return null;
        }

        if (formData.data.trim().length > 4096) {
            notifyError('Содержимое не должно превышать 4096 символов');
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

async function updateNoteStatus(id, status) {
    const url = `${window.location.origin}/notes/api/update/status/`;
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

async function deleteNote(id) {
    const url = `${window.location.origin}/notes/api/delete/`;
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