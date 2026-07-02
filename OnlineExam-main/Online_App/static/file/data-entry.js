document.addEventListener('DOMContentLoaded', () => {
    console.log('Dropdown script initialized for data-entry.');

    // Handle parent dropdowns
    const dropdowns = document.querySelectorAll('.dropdown7');

    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener('click', (event) => {
            console.log('Parent dropdown clicked:', dropdown);

            // Toggle active class on the clicked dropdown
            dropdown.classList.toggle('active');

            // Remove active class from other dropdowns
            dropdowns.forEach((item) => {
                if (item !== dropdown) {
                    item.classList.remove('active');
                }
            });

            // Prevent the click event from bubbling to the document
            event.stopPropagation();
        });
    });

    // Handle sub-dropdowns
    const subDropdowns = document.querySelectorAll('.sub-dropdown7');
    subDropdowns.forEach((subDropdown) => {
        subDropdown.addEventListener('click', (event) => {
            console.log('Sub-dropdown clicked:', subDropdown);

            event.stopPropagation(); // Prevent parent dropdown toggle
            subDropdown.classList.toggle('active');
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

    // Redirect to add_biology_question.html when clicking on Biology menu item
    const biologyMenuItem = document.getElementById('biologyMenuItem');
    biologyMenuItem.addEventListener('click', () => {
        const url = biologyMenuItem.getAttribute('data-url');  // Get the URL from the data attribute
        window.location.href = url;  // Redirect to the page
    });
});
