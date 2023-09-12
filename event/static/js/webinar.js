document.addEventListener("DOMContentLoaded", function() {
    var title = document.getElementById("title");
    var titleError = document.getElementById("titleError");
    var event_type = document.getElementById("event_type");
    var date = document.getElementById("date");
    var event_dateError = document.getElementById("event_dateError");
    var deadline = document.getElementById("deadline");
    var deadlineError = document.getElementById("deadlineError");
    var webinar = document.getElementById("webinar");
    var location = document.getElementById("location");
    var loc = document.getElementById("loc");
    var url_div = document.getElementById("url_div");
    var locationError = document.getElementById("locationError");
    var organizer_name = document.getElementById("organizer_name");
    var organizer_nameError = document.getElementById("organizer_nameError");
    var phone_number = document.getElementById("phone_number");
    var phone_numberError = document.getElementById("phone_numberError");
    var livestream = document.getElementById("livestream");
    var fee = document.getElementById("fee");
    var feeError = document.getElementById("feeError");
    var urlError = document.getElementById("urlError");
    var speaker_name = document.getElementById("speaker_name");
    var speakerError = document.getElementById("speakerError");
    
    title.addEventListener("input", function() {
        titleError.innerText = validateTitle(title.value);
    });
    date.addEventListener("input", function() {
        event_dateError.innerText = validateEvent_date(date.value);
    });
    event_type.addEventListener('change', function () {
        if (event_type.value === 'Online') {
            loc.style.display = 'none';
            url_div.style.display = 'block';
        } 
        else {
            loc.style.display = 'block';
            url_div.style.display = 'none';
        }
    });
    deadline.addEventListener("input", function() {
        deadlineError.innerText = validateDeadline(date.value,deadline.value);
    });
    speaker_name.addEventListener("input", function() {
        speakerError.innerText = validateSpeaker(speaker_name.value);
    });
    location.addEventListener("input", function() {
        locationError.innerText = validateLocation(location.value);
    });
    livestream.addEventListener("input", function() {
        urlError.innerText = validateUrl(livestream.value);
    });
    fee.addEventListener("input", function() {
        feeError.innerText = validateFee(fee.value);
    });
   
    phone_number.addEventListener("input", function() {
        phone_numberError.innerText = validateContact(phone_number.value);
    });
    organizer_name.addEventListener("input", function() {
        organizer_nameError.innerText = validateOrganizer(organizer_name.value);
    });
    
    webinar.addEventListener("submit", function(event) {
        // Validate all fields before submitting
        if (!validateForm()) {
            event.preventDefault(); // Prevent form submission if there are errors
        }
    });

    function validateForm() {
        
        if (titleError.innerText || event_dateError.innerText || locationError.innerText || deadlineError.innerText || organizer_nameError.innerText || contactError.innerText || feeError.innerText || urlError.innerText || speakerError.innerText ) {
            return false; // Return false to prevent form submission
        }

        return true; // All fields are valid, allow form submission
    }

    function validateTitle(title) {
        var pattern = /^[a-zA-Z,. ']*$/;
        if (!(pattern.test(title))) {
            return "Please enter only alphabets, space and commas";
            }
        title.innerText=title.toUpperCase;
        return "";
    }
    function validateLocation(location) {
        var pattern = /^[a-zA-Z,. ']*$/;
        if (!(pattern.test(location))) {
            return "Please enter only alphabets, space and commas";
            }
        return "";
    }
    function validateContact(phone_number) {
        var pattern = /^(?:(?:\+|00)1\s*[-]?)?(?:\([2-9][0-9]{2}\)|[2-9][0-9]{2})\s*[-]?(?:[2-9][0-9]{2})\s*[-]?(?:[0-9]{4}|\d{4}\s{0,2}[-]\s{0,2}\d{4})$/;
        if (!(pattern.test(phone_number))) {
            return "Please enter a valid phone number with 10 digits";
        }
        return "";
    }
    function validateFee(fee) {
        var pattern = /^[0-9]+$/;
        if (fee<0) {
            return "Please enter only positive numbers";
        }
        return "";
    }
    function validateUrl(livestream) {
        var pattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- .\/?%&=]*)?$/;
        if (!(pattern.test(livestream))) {
            return "Please enter a valid URL";
            }
        return "";
    }
    function validateOrganizer(organizer_name) {
        var pattern = /^[a-zA-Z,. ']*$/;
        if (!(pattern.test(organizer_name))) {
            return "Please enter only alphabets, space and commas";
            }
        return "";
    }
    function validateSpeaker(speaker_name) {
        var pattern = /^[a-zA-Z,. ']*$/;
        if (!(pattern.test(speaker_name))) {
            return "Please enter only alphabets, space and commas";
            }
        return "";
    }
    function validateEvent_date(date) {
        var currentDate = new Date();
        var eventDate = new Date(date);
    
        if (eventDate <= currentDate) {
            return "Please enter a date greater than the current date.";
        } else {
            return ""; // The input date is greater than the current date
        }
    } 
    function validateDeadline(event_date,deadline) {
        var todayDate = new Date();
        var deadlineDate = new Date(deadline);
        var eventDate = new Date(event_date);
        
        if (deadlineDate <= todayDate) {
            return "Please enter a date greater than the current date.";
        }
        if (eventDate <= deadlineDate) {
            return "Please enter a date less than the event date.";
        } 
        else {
            return ""; // The input date is greater than the current date
        }
    } 
    webinar.addEventListener("submit", function(event) {
        // Capitalize the title input value before submitting
        title.innerText = title.innerText.toUpperCase();
    });

    
});
