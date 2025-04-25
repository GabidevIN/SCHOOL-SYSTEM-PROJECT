function openDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    if (dialog) {
        dialog.showModal();
    }
}

function closeDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    if (dialog) {
        dialog.classList.add('fade-out');

        setTimeout(() => {
            dialog.classList.remove('fade-out');
            dialog.close();
        }, 500);
    }
}

function careerDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    if (dialog) {
        dialog.showModal();
    }
}

function carexitDialog(dialogId) {
    const dialog = document.getElementById(dialogId);
    if (dialog) {
        dialog.classList.add('fade-out');

        setTimeout(() => {
            dialog.classList.remove('fade-out');
            dialog.close();
        }, 500);
    }
}

function openCareerDialog() {
    const dialog = document.getElementById('popup-location');
    if (dialog) {
        dialog.showModal();
    }
}

function closeCareerDialog() {
    const dialog = document.getElementById('popup-location');
    if (dialog) {
        dialog.classList.add('fade-out');

        setTimeout(() => {
            dialog.classList.remove('fade-out');
            dialog.close();
        }, 500);
    }
}



