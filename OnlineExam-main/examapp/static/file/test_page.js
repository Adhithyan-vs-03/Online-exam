let timeLeft = parseInt(localStorage.getItem('test_timeLeft')) || 300; // Default to 5 minutes if no time is stored
let maxRefreshes = 5; // Define max refresh count, e.g. 5
let maxTabSwitches = 3; // Define max tab switches, e.g. 3

function startTimer() {
    let storedTimerRunning = localStorage.getItem('timer_running');

    if (storedTimerRunning === "true") {
        return; // Don't start a new timer if already running
    }

    localStorage.setItem('timer_running', "true");  // Mark timer as running

    let timerInterval = setInterval(function() {
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert("Time's up! Submitting your test.");
            document.getElementById("test-form").submit();
        } else {
            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;
            document.getElementById("timer").innerText = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

            timeLeft--;
            localStorage.setItem('test_timeLeft', timeLeft);
        }
    }, 1000);
}

// Check refresh count and submit if exceeded
function checkRefreshCount() {
    let refreshCount = parseInt(localStorage.getItem('refresh_count')) || 0;
    refreshCount += 1;
    localStorage.setItem('refresh_count', refreshCount);

    if (refreshCount > maxRefreshes) {
        alert("You have refreshed or left the page too many times. Submitting your test.");
        document.getElementById("test-form").submit();
    }
}

// Clear the localStorage when starting a new test
function clearTestData() {
    localStorage.removeItem('test_timeLeft');  
    localStorage.removeItem('refresh_count');  
    localStorage.removeItem('tab_switch_count');  
}

// Start a new test
function startNewTest() {
    clearTestData();  
    alert("Starting a new test...");
    window.location.href = "{% url 'test_page' %}";  
}

// Check tab switch count and submit if exceeded
function checkTabSwitch() {
    document.addEventListener("visibilitychange", function() {
        if (document.hidden) {
            let tabSwitchCount = parseInt(localStorage.getItem('tab_switch_count')) || 0;
            tabSwitchCount += 1;
            localStorage.setItem('tab_switch_count', tabSwitchCount);

            if (tabSwitchCount > maxTabSwitches) {
                alert("You switched tabs too many times. Submitting your test.");
                document.getElementById("test-form").submit();
            }
        }
    });
}

// Ensure data is loaded when page is loaded
window.onload = function() {
    checkRefreshCount();
    checkTabSwitch();
    startTimer();
};

// Store timer data before the page unloads
window.onbeforeunload = function() {
    if (typeof timeLeft !== "undefined") {
        localStorage.setItem('test_timeLeft', timeLeft);
    }
};

// Attach the form submission to the standard behavior
document.addEventListener("DOMContentLoaded", function() {
    let form = document.getElementById("test-form");
    if (form) {
        form.addEventListener("submit", function(event) {
            // No need to prevent default or handle AJAX, just submit normally
            localStorage.removeItem('timer_running'); // Optionally clear the timer state when submitting
        });
    }
});
