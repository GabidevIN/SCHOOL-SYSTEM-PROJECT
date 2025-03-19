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

function careersDialog() {
    const dialog = document.getElementById('popup-career');

    dialog.classList.add('fade-out');

    setTimeout(() => {
        dialog.classList.remove('fade-out');
        dialog.close();
    }, 500);
}