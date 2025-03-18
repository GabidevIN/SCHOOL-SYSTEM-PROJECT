function openDialog() {
    const dialog = document.getElementById('popup-location');
    dialog.showModal(); // Open modal
}

function closeDialog() {
    const dialog = document.getElementById('popup-location');

    // Add fade-out class
    dialog.classList.add('fade-out');

    // Wait for animation to complete before closing
    setTimeout(() => {
        dialog.classList.remove('fade-out'); // Remove class for future use
        dialog.close(); // Now close the dialog
    }, 500); // Matches CSS animation duration (0.5s)
}


function openDialog(dialogId) {
    document.getElementById(dialogId).showModal();
}

function closeDialog(dialogId) {
    document.getElementById(dialogId).close();
}