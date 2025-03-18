function openDialog() {
    const dialog = document.getElementById('popup-location');
    dialog.showModal();
}

function closeDialog() {
    const dialog = document.getElementById('popup-location');

    dialog.classList.add('fade-out');

    setTimeout(() => {
        dialog.classList.remove('fade-out');
        dialog.close();
    }, 500);
}


function openDialog(dialogId) {
    document.getElementById(dialogId).showModal();
}

function closeDialog(dialogId) {
    document.getElementById(dialogId).close();
}