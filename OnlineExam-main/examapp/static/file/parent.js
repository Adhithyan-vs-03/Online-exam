document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');

    // Select all parent dropdowns
    const dropdowns = document.querySelectorAll('.dropdown5');
    const subDropdowns = document.querySelectorAll('.sub-dropdown5');
    const packagesDropdown = document.querySelector('.dropdown5:nth-child(2)');
    const cardsContainer = document.querySelector('.cards-container3');
    const contactUsDropdown = document.querySelector('.dropdown5:nth-child(3)');
    const teacherContactDetails = document.getElementById('teacherContactDetails');

    if (!dropdowns.length) {
        console.error('No dropdowns found! Check your HTML structure or class names.');
    }

    // Toggle parent dropdown visibility
    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent click from bubbling up

            // Toggle the "active" class for the clicked dropdown
            dropdown.classList.toggle('active');

            // Close other dropdowns
            dropdowns.forEach((item) => {
                if (item !== dropdown) {
                    item.classList.remove('active');
                }
            });
        });
    });

    // Toggle sub-dropdown visibility
    subDropdowns.forEach((subDropdown) => {
        subDropdown.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent click from bubbling up
            subDropdown.classList.toggle('active');
        });
    });

    // Show/hide cards when "Packages" is clicked
    if (packagesDropdown) {
        packagesDropdown.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent bubbling up

            // Toggle the visibility of the cards container
            if (cardsContainer) {
                cardsContainer.style.display = cardsContainer.style.display === 'flex' ? 'none' : 'flex';
            }
        });
    }

    // Show/hide teacher contact details when "Contact Us" is clicked
    if (contactUsDropdown) {
        contactUsDropdown.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent bubbling up

            // Toggle the visibility of the teacher contact details
            if (teacherContactDetails) {
                teacherContactDetails.style.display = teacherContactDetails.style.display === 'block' ? 'none' : 'block';
            }
        });
    }

    // Close dropdowns and hide content when clicking outside
    document.addEventListener('click', () => {
        console.log('Clicked outside. Closing all dropdowns and hiding content.');

        // Remove the "active" class from all dropdowns and sub-dropdowns
        dropdowns.forEach((dropdown) => {
            dropdown.classList.remove('active');
        });

        subDropdowns.forEach((subDropdown) => {
            subDropdown.classList.remove('active');
        });

        // Hide cards container
        if (cardsContainer) {
            cardsContainer.style.display = 'none';
        }

        // Hide teacher contact details
        if (teacherContactDetails) {
            teacherContactDetails.style.display = 'none';
        }
    });
});
