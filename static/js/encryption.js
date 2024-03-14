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

async function encryptAES(password, data, initVector) {
    initVector = initVector || crypto.getRandomValues(new Uint8Array(16));
    let key = await crypto.subtle.importKey("raw", password, {name: "AES-CBC"}, false, ["encrypt"]);

    let encoded = new TextEncoder().encode(data);
    let encryptedData = await crypto.subtle.encrypt({name: "AES-CBC", iv: initVector}, key, encoded);
    return encryptedData;
}

async function decryptAES(password, encryptedData, initVector) {
    let key = await crypto.subtle.importKey("raw", password, {name: "AES-CBC"}, false, ["decrypt"]);

    let decryptedData = await crypto.subtle.decrypt({name: "AES-CBC", iv: initVector}, key, encryptedData);
    let decoded = new TextDecoder().decode(decryptedData);
    return decoded;
}