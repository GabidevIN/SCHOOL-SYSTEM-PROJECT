function filterStudents() {
    var filter = document.getElementById("bseeFilter").value.toUpperCase();
    var table = document.getElementById("studentTable");
    var rows = table.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var sectionCell = rows[i].getElementsByClassName("section")[0];
        if (sectionCell) {
            var sectionText = sectionCell.textContent || sectionCell.innerText;
            if (filter === "" || sectionText.toUpperCase().includes(filter)) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}
