function arrayBufferToHex(buffer) {
    return Array.from(new Uint8Array(buffer))
        .map(byte => byte.toString(16).padStart(2, '0'))
        .join('');
}

function hexToArrayBuffer(hex) {
    const bytes = new Uint8Array(hex.length / 2);

    for (let i = 0; i < bytes.length; i++) {
        bytes[i] = parseInt(hex.substr(i * 2, 2), 16);
    }

    return bytes;
}

async function generateKeyArgon2(password, salt, timeCost = 3, memoryCost = 65536, parallelism = 4, hashLen = 32) {
    salt = salt || crypto.getRandomValues(new Uint8Array(16));
    let key = await argon2.hash({
        pass: password,
        salt: salt,
        time: timeCost,
        mem: memoryCost,
        parallelism: parallelism,
        hashLen: hashLen,
        type: argon2.ArgonType.Argon2id
    });
    return key.hash;
}

async function encryptAES(password, data, salt, iv) {
    salt = salt || crypto.getRandomValues(new Uint8Array(16));
    iv = iv || crypto.getRandomValues(new Uint8Array(16));
    let keyMaterial = await generateKeyArgon2(password, salt);
    let key = await crypto.subtle.importKey("raw", keyMaterial, {name: "AES-CBC"}, false, ["encrypt"]);

    let encoded = new TextEncoder().encode(data);
    let encryptedData = await crypto.subtle.encrypt({name: "AES-CBC", iv: iv}, key, encoded);
    return encryptedData;
}

async function decryptAES(password, encryptedData, salt, iv) {
    let keyMaterial = await generateKeyArgon2(password, salt);
    let key = await crypto.subtle.importKey("raw", keyMaterial, {name: "AES-CBC"}, false, ["decrypt"]);

    let decryptedData = await crypto.subtle.decrypt({name: "AES-CBC", iv: iv}, key, encryptedData);
    let decoded = new TextDecoder().decode(decryptedData);
    return decoded;
}
