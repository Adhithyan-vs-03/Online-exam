function validateForm(event) {
    let valid = true;

    // Reset error messages
    document.getElementById('firstname-error').style.display = 'none';
    document.getElementById('lastname-error').style.display = 'none';
    document.getElementById('email-error').style.display = 'none';
    document.getElementById('number-error').style.display = 'none';
    document.getElementById('guardianname-error').style.display = 'none';
    document.getElementById('gnumber-error').style.display = 'none';
    document.getElementById('pinnumber-error').style.display = 'none';

    // Validate First Name
    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const email = document.getElementById('email').value;
    const number = document.getElementById('number').value;
    const guardianname = document.getElementById('guardianname').value;
    const gnumber = document.getElementById('gnumber').value;
    const pinnumber = document.getElementById('pinnumber').value;
    const namePattern = /^[A-Za-z]+$/;

    if (!firstname.match(namePattern)) {
        document.getElementById('firstname-error').style.display = 'inline';
        valid = false;
    }

    // Validate Last Name
    if (!lastname.match(namePattern)) {
        document.getElementById('lastname-error').style.display = 'inline';
        valid = false;
    }

    // Validate Email
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!email.match(emailPattern)) {
        document.getElementById('email-error').style.display = 'inline';
        valid = false;
    }

    // Validate Mobile Number
    if (number.length !== 10) {
        document.getElementById('number-error').style.display = 'inline';
        valid = false;
    }

    // Validate Guardian Name
    if (!guardianname.match(namePattern)) {
        document.getElementById('guardianname-error').style.display = 'inline';
        valid = false;
    }

    // Validate Guardian Number
    if (gnumber.length !== 10) {
        document.getElementById('gnumber-error').style.display = 'inline';
        valid = false;
    }

    // Validate PIN Code
    if (pinnumber.length !== 6) {
        document.getElementById('pinnumber-error').style.display = 'inline';
        valid = false;
    }

    if (!valid) {
        event.preventDefault(); // Prevent form submission if validation fails
        alert("Please correct the errors in the form.");
    }
}

// Attach the validation function to the form's







