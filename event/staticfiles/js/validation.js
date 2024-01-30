document.addEventListener("DOMContentLoaded", function() {
        var emailInput = document.getElementById("email");
        var emailError = document.getElementById("emailError");
        
        var passwordInput = document.getElementById("password");
        var passwordError = document.getElementById("passwordError");
        if (emailInput === ""  || passwordInput === "" ) {
            errorElement.innerText = "Please fill every fields";
        }
        emailInput.addEventListener("input", function() {
            validateField(emailInput, emailError, validateEmail);
        });

        

        passwordInput.addEventListener("input", function() {
            validateField(passwordInput, passwordError, validatePassword);
        });


        function validateField(input, errorElement, validationFunction) {
            var errorMessage = validationFunction(input.value);
            errorElement.innerText = errorMessage;
        }

        function validateEmail(email) {
            var pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!pattern.test(email)) {
                return "Invalid email";
            }
            return "";
        }

        function validateName(name) {
            var pattern = /^[A-Za-z\s]+$/;
            if (!pattern.test(name)) {
                return "Invalid name: Please use only letters and spaces.";
            }
            if (/\d/.test(name)) {
                return "Invalid name: Cannot contain numbers.";
            }    
            return "";
        }

        function validatePassword(password) {
            var pattern = /^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[A-Z]).{8,}$/;
            if (!pattern.test(password)) {
                if ((password.length < 8)||(!/[0-9]/.test(password))||(!/[A-Z]/.test(password))||(!/[!@#$%^&*]/.test(password))) {
                    return "Please enter at least 8 characters, at least 1 number, at least 1 symbol (!@#$%^&*), at least 1 capital letter";
                }
                return errorMessage;
        }
        return "";
    }

        function validateConfirmPassword(confirmPassword) {
            var password = passwordInput.value;
            if (confirmPassword !== password) {
                return "Passwords do not match";
            }
            return "";
        }
    });
