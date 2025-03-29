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

<<<<<<< HEAD
function closeDialog(dialogId) {
    document.getElementById(dialogId).close();
}

function openDialogs() {
    const dialog = document.getElementById('popup-location');
    dialog.showModal();
}

function closeDialogs() {
    const dialog = document.getElementById('popup-location');
=======
function careersDialog() {
    const dialog = document.getElementById('popup-career');
>>>>>>> ef63f8fb72821e2968a620f539ccf52c354d99ea

    dialog.classList.add('fade-out');

    setTimeout(() => {
        dialog.classList.remove('fade-out');
        dialog.close();
    }, 500);
<<<<<<< HEAD
}


function openDialogs(dialogId) {
    document.getElementById(dialogId).showModal();
}

function closeDialogs(dialogId) {
    document.getElementById(dialogId).close();
=======
>>>>>>> ef63f8fb72821e2968a620f539ccf52c354d99ea
}