function sendMail(contactForm) {
    emailjs.send("gmail", "yamiihomecooking", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "recipe_request": contactForm.help-request.value
    });
}