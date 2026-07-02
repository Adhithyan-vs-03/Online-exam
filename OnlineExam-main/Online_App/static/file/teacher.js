document.addEventListener("DOMContentLoaded", () => {
    // Function to toggle visibility of sections
    function toggleSection(sectionId) {
        document.querySelectorAll(".form-container").forEach((sec) => {
            if (sec.id !== sectionId) {
                sec.style.display = "none"; // Hide all other sections
            }
        });

        const section = document.getElementById(sectionId);
        if (section) {
            section.style.display = section.style.display === "block" ? "none" : "block";
        }
    }

    // Profile Section Toggle
    const profileMenu = document.getElementById("profile-link");
    const profileSection = document.getElementById("teacher-profile-section");

    if (profileMenu && profileSection) {
        profileMenu.addEventListener("click", function (event) {
            event.stopPropagation();
            toggleSection("teacher-profile-section");
        });
    }

    // Hide profile section when clicking outside
    document.addEventListener("click", function (event) {
        if (
            profileSection.style.display === "block" &&
            !profileMenu.contains(event.target) &&
            !profileSection.contains(event.target)
        ) {
            profileSection.style.display = "none";
        }
    });

    // Prevent click inside the profile form from closing it
    if (profileSection) {
        profileSection.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    }

    // Student Details Section Click Event
    const studentDetailsLink = document.getElementById("student-details-link");
    if (studentDetailsLink) {
        studentDetailsLink.addEventListener("click", (event) => {
            event.preventDefault();
            window.location.href = "/marks/";
        });
    }

    // Exam Schedule Section Click Event
    const examMenu = document.getElementById("exam-link");
    const examSection = document.getElementById("exam-schedule-section");

    if (examMenu && examSection) {
        examMenu.addEventListener("click", (event) => {
            event.stopPropagation();
            toggleSection("exam-schedule-section");
        });

        // Hide Exam Schedule Management when clicking outside
        document.addEventListener("click", function (event) {
            if (
                examSection.style.display === "block" &&
                !examMenu.contains(event.target) &&
                !examSection.contains(event.target)
            ) {
                examSection.style.display = "none";
            }
        });

        // Prevent closing when clicking inside the exam section
        examSection.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    }

    // Exam Form Submission - Reload Page After Submission
    const examForm = document.getElementById("exam-form");
    if (examForm) {
        examForm.addEventListener("submit", () => {
            setTimeout(() => {
                window.location.reload();
            }, 500);
        });
    }
});
