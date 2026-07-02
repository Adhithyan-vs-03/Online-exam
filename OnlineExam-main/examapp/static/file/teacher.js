document.addEventListener('DOMContentLoaded', () => {
    console.log('Dropdown script initialized for teacher.');

    // Handle parent dropdowns
    const dropdowns = document.querySelectorAll('.dropdown9');

    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener('click', (event) => {
            console.log('Parent dropdown clicked:', dropdown);

            // Toggle active class on the clicked dropdown
            dropdown.classList.toggle('active');

            // Remove active class from other dropdowns
            dropdowns.forEach((otherDropdown) => {
                if (otherDropdown !== dropdown) {
                    otherDropdown.classList.remove('active');
                }
            });

            // Prevent the click event from bubbling to the document
            event.stopPropagation();
        });
    });

    // Handle sub-dropdowns
    const subDropdowns = document.querySelectorAll('.sub-dropdown9');
    subDropdowns.forEach((subDropdown) => {
        subDropdown.addEventListener('click', (event) => {
            console.log('Sub-dropdown clicked:', subDropdown);

            // Toggle active class for sub-dropdown
            subDropdown.classList.toggle('active');

            // Prevent the click event from bubbling to the parent dropdown
            event.stopPropagation();
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        console.log('Clicked outside. Closing all dropdowns.');
        dropdowns.forEach((dropdown) => {
            dropdown.classList.remove('active');
        });

        subDropdowns.forEach((subDropdown) => {
            subDropdown.classList.remove('active');
        });
    });
});
