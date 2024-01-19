document.addEventListener("DOMContentLoaded", function() {
    var name = document.getElementById("name");
    var nameError = document.getElementById("nameError");
    var locations = document.getElementById("locations");
    var locationsError = document.getElementById("locationsError");
    var start_range = document.getElementById("start_range");
    var start_rangeError = document.getElementById("start_rangeError");
    var end_range = document.getElementById("end_range");
    var end_rangeError = document.getElementById("end_rangeError");
    var image = document.getElementById("image");
    var imageError = document.getElementById("imageError");
    var services = document.getElementById("data-input");
    var service = document.getElementById("service");
    var servicesError = document.getElementById("servicesError");
    name.addEventListener("input", function() {
        nameError.innerText = validateName(name.value);
    });
    



    function validateForm() {
        
        if (nameError.innerText || categoryError.innerText || start_rangeError.innerText || end_rangeError.innerText || locationsError.innerText) {
            return false; // Return false to prevent form submission
        }

        return true; // All fields are valid, allow form submission
    }

    function validateName(name) {
        var pattern = /^[a-zA-Z,. ']*$/;
        if (!(pattern.test(name))) {
            return "Please enter only alphabets, numbers, space and commas";
            }
        return "";
    }

    
});
