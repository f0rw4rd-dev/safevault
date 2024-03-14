async function getSaltAndInitVector(email) {
    try {
        const response = await fetch(`${window.location.origin}/users/api?email=${encodeURIComponent(email)}`);
        if (!response.ok) {
            throw new Error('Произошла ошибка при получении данных с сервера');
        }

        const data = await response.json();
        if (data.salt && data.init_vector) {
            return {
                salt: hexToArrayBuffer(data.salt),
                initVector: hexToArrayBuffer(data.init_vector)
            };
        } else {
            throw new Error('Получены не все данные с сервера');
        }
    } catch (error) {
        console.error('Произошла ошибка при получении данных с сервера', error);
        return null;
    }
}
