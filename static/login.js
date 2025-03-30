function locationDialog() {
    const dialog = document.getElementById('popup-location');
    dialog.showModal();
}

function locationsDialog() {
    const dialog = document.getElementById('popup-location');

    dialog.classList.add('fade-out');

    setTimeout(() => {
        dialog.classList.remove('fade-out');
        dialog.close();
    }, 500);
}

function careerDialog() {
    const dialog = document.getElementById('popup-career');
    dialog.showModal();
}

function closeDialog(dialogId) {
    document.getElementById(dialogId).close();
}

function openDialogs() {
    const dialog = document.getElementById('popup-location');
    dialog.showModal();
}

function closeDialogs() {
    const dialog = document.getElementById('popup-location');

    dialog.classList.add('fade-out');

    setTimeout(() => {
        dialog.classList.remove('fade-out');
        dialog.close();
    }, 500);
}


function openDialogs(dialogId) {
    document.getElementById(dialogId).showModal();
}

function closeDialogs(dialogId) {
    document.getElementById(dialogId).close();
}