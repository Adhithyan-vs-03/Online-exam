document.addEventListener('DOMContentLoaded', () => {
    console.log('Dropdown script initialized');

    // Handle parent dropdowns
    const dropdowns = document.querySelectorAll('.dropdown8');
    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener('click', () => {
            console.log('Parent dropdown clicked:', dropdown);

            // Toggle active class on the clicked dropdown
            dropdown.classList.toggle('active');

            // Remove active class from other dropdowns
            dropdowns.forEach((item) => {
                if (item !== dropdown) {
                    item.classList.remove('active');
                }
            });
        });
    });

    // Handle sub-dropdowns
    const subDropdowns = document.querySelectorAll('.sub-dropdown8');
    subDropdowns.forEach((subDropdown) => {
        subDropdown.addEventListener('click', (event) => {
            console.log('Sub-dropdown clicked:', subDropdown);

            event.stopPropagation(); // Prevent parent dropdown toggle
            subDropdown.classList.toggle('active');
        });
    });
});

