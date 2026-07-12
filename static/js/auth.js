document.addEventListener("DOMContentLoaded", function () {

    // Add Bootstrap shadow

    document.querySelectorAll(".form-control").forEach(function (input) {

        input.classList.add("shadow-sm");

    });

    // Password Toggle

    const toggle = document.getElementById("togglePassword");

    const password = document.querySelector("input[type='password']");

    if (toggle && password) {

        toggle.addEventListener("click", function () {

            if (password.type === "password") {

                password.type = "text";

                toggle.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';

            } else {

                password.type = "password";

                toggle.innerHTML = '<i class="fa-solid fa-eye"></i>';

            }

        });

    }

    // Loading Button

    const form = document.getElementById("loginForm");

    const button = document.getElementById("loginButton");

    if (form && button) {

        form.addEventListener("submit", function () {

            button.disabled = true;

            button.innerHTML =

                '<span class="spinner-border spinner-border-sm me-2"></span>Signing In...';

        });

    }

});