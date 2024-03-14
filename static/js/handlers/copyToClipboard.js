async function copyTextToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
    } catch (err) {

    }
}

function setupCopyTextToClipboard() {
    document.querySelectorAll('.btn-copy').forEach(button => {
        button.addEventListener('click', function (event) {
            const input = this.previousElementSibling;
            copyTextToClipboard(input.value);
        });
    });
}