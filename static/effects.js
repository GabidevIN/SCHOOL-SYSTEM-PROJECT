document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".menu a, .nav");
    const loader = document.createElement("div");
    loader.classList.add("loader");
    loader.innerHTML = "Loading...";
    document.body.appendChild(loader);

    setTimeout(() => {
        document.body.classList.add("loaded");
    }, 100);

    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const href = this.getAttribute("href");

            document.body.classList.remove("loaded");
            loader.classList.add("active");

            setTimeout(() => {
                window.location.href = href;
            }, 500);
        });
    });

    window.addEventListener("pageshow", function () {
        document.body.classList.add("loaded");
        loader.classList.remove("active");
    });
});