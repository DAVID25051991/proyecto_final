document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector("#menu-toggle");
    const menu = document.querySelector("#layout-menu");
    const toggleText = document.querySelector("#toggle-text");

    menuToggle.addEventListener("click", function () {
        menu.classList.toggle("menu-collapsed");
        toggleText.textContent = menu.classList.contains("menu-collapsed") ? "Empleados" : "Cerrar";
    });
});
