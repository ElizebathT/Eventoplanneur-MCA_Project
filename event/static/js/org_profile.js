document.addEventListener("DOMContentLoaded", function() {
    var profile = document.getElementById("profile");
        var college = document.getElementById("college");
        var aicte = document.getElementById("aicte");
        var nameInput = document.getElementById("name");
        var nameError = document.getElementById("nameError");
        var phone_number = document.getElementById("phone_number");
        var phone_numberError = document.getElementById("phone_numberError");
        var location = document.getElementById("location");
        var locationError = document.getElementById("locationError");
        var website = document.getElementById("website");
        var websiteError = document.getElementById("websiteError");
        var departments = document.getElementById("departments");
        var departmentsError = document.getElementById("departmentsError");
        var programs_offered = document.getElementById("programs_offered");
        var programs_offeredError = document.getElementById("programs_offeredError");
        var address = document.getElementById("address");
        var addressError = document.getElementById("addressError");
        var aicteError = document.getElementById("aicteError");
        if (nameInput === "" || phone_number === "" || location === "") {
            errorElement.innerText = "Please fill every fields";
        }

        nameInput.addEventListener("input", function() {
            validateField(nameInput, nameError, validateName);
        });

        phone_number.addEventListener("input", function() {
            validateField(phone_number,phone_numberError, validatePhonenumber);
        });

        location.addEventListener("input", function() {
            validateField(location, locationError, validateLocation);
        });

        address.addEventListener("input", function() {
            validateField(address, addressError, validateAddress);
        });

        website.addEventListener("input", function() {
            validateField(website, websiteError, validateWebsite);
        });

        website.addEventListener("input", function() {
            validateWebsiteInput();
        });
        
        // Function to validate the "website" input field
        function validateWebsiteInput() {
            isValidWebsite(website.value, websiteError);
        }
        aicte.addEventListener("input", function() {
            isValidateAicte(aicte, aicteError);
        });
        aicte.addEventListener("input", function() {
            validateField(aicte, aicteError, validateAicte);
        });
        

        college.addEventListener("change",toggleFieldVisibility);

    profile.addEventListener("submit", function(event) {
        // Validate all fields before submitting
        if (!validateForm()) {
            event.preventDefault(); // Prevent form submission if there are errors
        }
    });
    function validateForm() {
        
        if (nameError.innerText || phone_numberError.innerText || locationError.innerText || websiteError.innerText || departmentsError.innerText ||aicteError.innerText || programs_offeredError.innerText || accreditationError.innerText ) {
            return false; // Return false to prevent form submission
        }

        return true; // All fields are valid, allow form submission
    }
        function toggleFieldVisibility() {
            // Check if the "College" checkbox is checked
            if (college.checked) {
                aicte.style.display = "block";
            } else {
                aicte.style.display = "none";
            }
        }

        function validateField(input, errorElement, validationFunction) {
            var errorMessage = validationFunction(input.value);
            errorElement.innerText = errorMessage;
        }
        
    async function isValidWebsite(website, websiteError) {
        // var response = await fetch(website);
        // if (response.status === 200) {
        // websiteError.innerText="The website exists.";
        // } else {
        //     websiteError.innerText="The website does not exist.";
        // }


        
    // var urlRegex = /^(https?:\/\/)?([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})+)(\/[^\s]*)?$/;
    // if (!urlRegex.test(website)) {
    //     websiteError.innerText = "Invalid Website"; // Invalid URL format
    //     return;
    // }
    // var xhr = new XMLHttpRequest();
    // xhr.timeout = 10000; // Set a timeout of 10 seconds (in milliseconds)
    // xhr.open("HEAD", website, true); // Set to asynchronous (true)

    // xhr.onload = function () {
    //     console.log(xhr.status)
    //     if (xhr.status === 200) {
    //         websiteError.innerText = "Website is valid"; // Website is accessible
    //     } else {
    //         websiteError.innerText = "Website does not exist"; // Website is not accessible (e.g., 404 Not Found)
    //     }
    // };

    // // xhr.onerror = function () {
    // //     websiteError.innerText = "Network error occurred"; // Network error
    // // };

    // xhr.ontimeout = function () {
    //     websiteError.innerText = "Request timed out"; // Request timed out
    // };

    // xhr.send();
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

        function validatePhonenumber(phone_number) {
            var pattern = /^(?:(?:\+|00)1\s*[-]?)?(?:\([2-9][0-9]{2}\)|[2-9][0-9]{2})\s*[-]?(?:[2-9][0-9]{2})\s*[-]?(?:[0-9]{4}|\d{4}\s{0,2}[-]\s{0,2}\d{4})$/;
            if (!(pattern.test(phone_number))) {
                return "Please enter a valid phone number with 10 digits";
                }
            return "";
        }

        function validateLocation(location) {
            var pattern = /^[A-Za-z\s]+$/;
            if (/\d/.test(location)) {
                return "Invalid location: Cannot contain numbers.";
            } 
            if (!pattern.test(location)) {
                return "Invalid location: Please use only letters and spaces.";
            } 
            return "";
        }

        function validateWebsite(website) {
            var pattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?$/;
            if (!(pattern.test(website))) {
                return "Please enter a valid URL";
                }
            return "";
        }

        function validateAddress(address) {
            var pattern =/^[a-zA-Z, 0-9.]*$/;
            if (!pattern.test(address)) {
                return "Please enter only alphabets, numbers, space and commas";
                }
            return "";
        }

        function validateAicte(aicte) {
            var pattern = /^[0-9 -]*$/;
            if (!(pattern.test(aicte))) {
                return "Please enter number and - only";
                }
            return "";
        }
        function isValidateAicte(aicte, aicteError) {
           
        }
});
