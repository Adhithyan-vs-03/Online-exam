document.addEventListener("DOMContentLoaded", () => {
    console.log("Script initialized");

    // Elements
    const profileButton = document.getElementById("profileButton");
    const profileFormContainer = document.querySelector(".profile-form-container");
    const packagesDropdown = document.getElementById("packagesDropdown");
    const cardsContainer = document.getElementById("cardsContainer");
    const resultButton = document.getElementById("resultButton");
    const resultFormContainer = document.getElementById("result-form-container");
    const examDropdown = document.querySelector(".dropdown8");
    const examDropdownMenu = examDropdown?.querySelector(".dropdown-menu8");

    if (!examDropdownMenu) {
        console.error("Exam dropdown menu not found. Check HTML structure.");
    } else {
        examDropdownMenu.style.display = "none";
    }

    // List of all sections to manage visibility
    const sections = [profileFormContainer, cardsContainer, resultFormContainer];

    // Function to toggle visibility and hide others
    function toggleVisibility(element) {
        if (!element) return;
        sections.forEach((sec) => sec !== element && sec && (sec.style.display = "none"));
        element.style.display = element.style.display === "none" || !element.style.display ? "block" : "none";
    }

    // Attach event listeners
    profileButton?.addEventListener("click", (event) => {
        event.stopPropagation();
        toggleVisibility(profileFormContainer);
    });

    packagesDropdown?.addEventListener("click", (event) => {
        event.stopPropagation();
        toggleVisibility(cardsContainer);
    });

    resultButton?.addEventListener("click", (event) => {
        event.stopPropagation();
        toggleVisibility(resultFormContainer);
    });

    examDropdown?.addEventListener("click", (event) => {
        event.stopPropagation();
        if (examDropdownMenu) {
            examDropdownMenu.style.display = examDropdownMenu.style.display === "none" ? "block" : "none";
            console.log("Exam dropdown toggled:", examDropdownMenu.style.display);
        }
    });

    

    // Hide all sections when clicking outside
    document.addEventListener("click", (event) => {
        if (!event.target.closest(".profile-form-container, .cards-container, .result-form-container, .dropdown8, .dropdown-menu8")) {
            sections.forEach((sec) => sec && (sec.style.display = "none"));
            examDropdownMenu && (examDropdownMenu.style.display = "none");
        }
    });

    // Handle dropdown toggling
    document.querySelectorAll(".dropdown8").forEach((dropdown) => {
        dropdown.addEventListener("click", () => {
            console.log("Parent dropdown clicked:", dropdown);
            dropdown.classList.toggle("active");
            document.querySelectorAll(".dropdown8").forEach((item) => {
                if (item !== dropdown) item.classList.remove("active");
            });
        });
    });

    // Sub-dropdown toggle
    document.querySelectorAll(".sub-dropdown8").forEach((subDropdown) => {
        subDropdown.addEventListener("click", (event) => {
            console.log("Sub-dropdown clicked:", subDropdown);
            event.stopPropagation();
            subDropdown.classList.toggle("active");
        });
    });
});
