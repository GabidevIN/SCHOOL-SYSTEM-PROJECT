function filterStudents() {
    const selected = document.getElementById("bscpeFilter").value;
    const rows = document.querySelectorAll("#studentTable tr");

    rows.forEach(row => {
        const sectionText = row.querySelector(".section").textContent;
        if (!selected || sectionText === selected) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}