document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded Successfully!");

    // Selecting all dropdowns
    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener("click", function (event) {
            event.stopPropagation(); // Prevent event bubbling

            // Find the associated dropdown menu
            const menu = this.querySelector(".dropdown-menu");
            if (!menu) return;

            // Close all other dropdowns before opening this one
            document.querySelectorAll(".dropdown-menu").forEach(otherMenu => {
                if (otherMenu !== menu) {
                    otherMenu.classList.remove("show");
                }
            });

            // Toggle the clicked dropdown menu
            menu.classList.toggle("show");
        });
    });

    // Prevent closing when clicking inside the menu
    document.querySelectorAll(".dropdown-menu").forEach(menu => {
        menu.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener("click", function () {
        document.querySelectorAll(".dropdown-menu").forEach(menu => {
            menu.classList.remove("show");
        });
    });

    // Handling Exam Details & Package Management
    const examDetailsMenu = document.getElementById("exam-details-menu");
    const examDetailsSection = document.getElementById("examDetailsSection");
    const manageMenu = document.getElementById("manage-menu");
    const packageManagement = document.getElementById("package-management");
    const numberBox = document.querySelector(".number-box");
    const staffsMenu = document.getElementById("staffs-menu");
    const studentMenu = document.getElementById("student-menu");
    const examForm = document.getElementById("exam-form");

    // Initially hide the exam details section
    if (examDetailsSection) {
        examDetailsSection.style.display = "none";
    }

    function hideNumberBoxes() {
        if (numberBox) numberBox.style.display = "none";
    }

    function showNumberBoxes() {
        if (numberBox) numberBox.style.display = "flex";
    }

    // Function to toggle sections
    function toggleSection(menu, sectionToShow) {
        if (!menu || !sectionToShow) return;

        menu.addEventListener("click", function (event) {
            event.stopPropagation();

            if (sectionToShow.style.display === "block") {
                sectionToShow.style.display = "none";
                showNumberBoxes();
            } else {
                sectionToShow.style.display = "block";
                hideNumberBoxes();

                // Hide other sections
                [examDetailsSection, packageManagement].forEach(section => {
                    if (section !== sectionToShow) {
                        section.style.display = "none";
                    }
                });
            }
        });
    }

    toggleSection(examDetailsMenu, examDetailsSection);
    toggleSection(manageMenu, packageManagement);

    // Hide sections when clicking outside
    document.addEventListener("click", function (event) {
        if (!event.target.closest("#examDetailsSection") && event.target.id !== "exam-details-menu") {
            if (examDetailsSection) examDetailsSection.style.display = "none";
            showNumberBoxes();
        }

        if (!event.target.closest("#package-management") && event.target.id !== "manage-menu") {
            if (packageManagement) packageManagement.style.display = "none";
            showNumberBoxes();
        }
    });

    // Navigate to Staff List
    if (staffsMenu) {
        staffsMenu.addEventListener("click", function (event) {
            event.stopPropagation();
            window.location.href = "/staffs/";
        });
    }

    // Navigate to Student List
    if (studentMenu) {
        studentMenu.addEventListener("click", function (event) {
            event.stopPropagation();
            window.location.href = "/students/";
        });
    }

    // Hide package cards when clicking "Add Exam"
    if (examForm) {
        examForm.addEventListener("submit", function () {
            // Hide package management when adding an exam
            if (packageManagement) {
                packageManagement.style.display = "none";
            }

            // Hide number box if needed
            if (numberBox) {
                numberBox.style.display = "none";
            }
        });
    }
});
