document.addEventListener('DOMContentLoaded', async (event) => {
    const email = getCookie('email');
    const encryptionKey = getCookie('encryptionKey');

    if (email === null || encryptionKey === null) {
        notifyError('Произошла непредвиденная ошибка');
        window.location.href = `${window.location.origin}/users/logout`;
        return null;
    }

    await decryptData(encryptionKey);

    setupEditDocumentButtons(encryptionKey);
    setupCopyTextToClipboard();
    setupFormSubmit('id_form_add_document', encryptionKey);
    setupFormSubmit('id_form_edit_document', encryptionKey);
});

async function decryptData(encryptionKey) {
    const elements = document.querySelectorAll('.record_document');
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

function setupEditDocumentButtons(encryptionKey) {
    document.querySelectorAll('.btn-edit-document').forEach(button => {
        button.addEventListener('click', async (e) => {
            const data = {
                title: e.currentTarget.getAttribute('data-title'),
                document_number: e.currentTarget.getAttribute('data-document-number'),
                issuing_authority: e.currentTarget.getAttribute('data-issuing-authority'),
                issue_date_custom: e.currentTarget.getAttribute('data-issue-date'),
                expiration_date_custom: e.currentTarget.getAttribute('data-expiration-date'),
                extra_data: e.currentTarget.getAttribute('data-extra-data'),
            };

            const form = document.getElementById('id_form_edit_document');

            const favorite = e.currentTarget.getAttribute('data-status') === '1';
            const initVector = e.currentTarget.getAttribute('data-init-vector');
            const id = e.currentTarget.getAttribute('data-id');

            for (const key of Object.keys(data)) {
                if (form.elements[key]) {
                    console.log(data[key]);
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
            document_number: form.document_number.value,
            issuing_authority: form.issuing_authority.value,
            issue_date: form.issue_date_custom.value,
            expiration_date: form.expiration_date_custom.value,
            extra_data: form.extra_data.value
        };

        // Check data
        if (formData.title.trim().length === 0
            || formData.document_number.trim().length === 0) {
            notifyError('Все обязательные поля должны быть заполнены');
            return null;
        }

        if (formData.title.trim().length > 48) {
            notifyError('Название заголовка не должно превышать 48 символов');
            return null;
        }

        if (formData.document_number.trim().length > 32) {
            notifyError('Номер документа не должен превышать 32 символа');
            return null;
        }

        if (formData.issuing_authority.trim().length > 256) {
            notifyError('Название органа выдачи не должно превышать 256 символов');
            return null;
        }

        if (formData.extra_data.trim().length > 4096) {
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

async function updateDocumentStatus(id, status) {
    const url = `${window.location.origin}/documents/api/update/status/`;
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

async function deleteDocument(id) {
    const url = `${window.location.origin}/documents/api/delete/`;
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