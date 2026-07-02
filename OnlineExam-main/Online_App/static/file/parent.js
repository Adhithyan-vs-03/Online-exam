document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");

    // Select elements
    const dropdowns = document.querySelectorAll(".dropdown5");
    const subDropdowns = document.querySelectorAll(".sub-dropdown5");
    const packagesDropdown = document.querySelector(".dropdown5:nth-child(2)");
    const cardsContainer = document.querySelector(".cards-container3");
    const contactUsDropdown = document.querySelector(".dropdown5:nth-child(3)");
    const teacherContactDetails = document.getElementById("teacherContactDetails");
    const examDetailsMenu = document.getElementById("examDetailsMenu");
    const examDetailsSection = document.getElementById("exam-details-section");

    if (!dropdowns.length) {
        console.error("No dropdowns found! Check your HTML structure or class names.");
    }

    // Toggle parent dropdown visibility
    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener("click", (event) => {
            event.stopPropagation();
            dropdown.classList.toggle("active");

            // Close other dropdowns
            dropdowns.forEach((item) => {
                if (item !== dropdown) {
                    item.classList.remove("active");
                }
            });
        });
    });

    // Redirect to parent result page when "Exam Results" is clicked
    const examResultsMenu = document.getElementById("examResultsMenu");
    if (examResultsMenu) {
        examResultsMenu.addEventListener("click", () => {
            const url = examResultsMenu.getAttribute("data-url");
            window.location.href = url;
        });
    }

    // Show Exam Details section when clicking "Exam Details" in the dropdown
    if (examDetailsMenu) {
        examDetailsMenu.addEventListener("click", (event) => {
            event.stopPropagation();
            console.log("Exam Details menu clicked");

            if (cardsContainer) cardsContainer.style.display = "none";
            if (examDetailsSection) examDetailsSection.style.display = "block";
        });
    }

    // Hide "Exam Details" when clicking outside
    document.addEventListener("click", (event) => {
        console.log("Clicked outside. Closing all dropdowns and hiding content.");

        dropdowns.forEach((dropdown) => dropdown.classList.remove("active"));
        subDropdowns.forEach((subDropdown) => subDropdown.classList.remove("active"));

        if (cardsContainer) cardsContainer.style.display = "none";
        if (teacherContactDetails) teacherContactDetails.style.display = "none";

        // Check if the click happened outside the "Exam Details" section
        if (examDetailsSection && !examDetailsSection.contains(event.target) && event.target !== examDetailsMenu) {
            examDetailsSection.style.display = "none";
        }
    });

    // Show/hide cards when "Packages" is clicked
    if (packagesDropdown) {
        packagesDropdown.addEventListener("click", (event) => {
            event.stopPropagation();
            if (cardsContainer) {
                cardsContainer.style.display = cardsContainer.style.display === "flex" ? "none" : "flex";
            }
        });
    }

    
    document.addEventListener("DOMContentLoaded", () => {
        console.log("DOM fully loaded and parsed");
    
        const packagesMenu = document.getElementById("packagesMenu");
    
        if (packagesMenu) {
            packagesMenu.addEventListener("click", () => {
                const url = packagesMenu.getAttribute("data-url");
                if (url) {
                    window.location.href = url;
                } else {
                    console.error("Packages menu URL not found.");
                }
            });
        }
    });
    




    // Show/hide teacher contact details when "Contact Us" is clicked
    if (contactUsDropdown) {
        contactUsDropdown.addEventListener("click", (event) => {
            event.stopPropagation();
            if (teacherContactDetails) {
                teacherContactDetails.style.display = teacherContactDetails.style.display === "block" ? "none" : "block";
            }
        });
    }
});
