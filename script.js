// Wait until the entire HTML page is loaded before running the script
document.addEventListener('DOMContentLoaded', () => {

    // Get references to all the clickable elements from the HTML
    const playButton = document.getElementById('play-button');
    const settingsButton = document.getElementById('settings-button');
    const uploadButton = document.getElementById('upload-button');
    const infoButton = document.getElementById('info-button');

    // --- Define what happens when each button is clicked ---

    playButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevents the link from trying to navigate
        play();
    });

    settingsButton.addEventListener('click', (event) => {
        event.preventDefault();
        settings();
    });

    uploadButton.addEventListener('click', (event) => {
        event.preventDefault();
        upload();
    });

    infoButton.addEventListener('click', (event) => {
        event.preventDefault();
        info();
    });

    // --- Your original functions ---
    // We use console.log, which is the browser equivalent of p5's print()

    function play() {
        alert("Play button clicked!"); // Optional: show a popup
    }

    function settings() {
        console.log("settings button clicked");
    }

    function upload() {
        console.log("upload button clicked");
    }

    function info() {
        console.log("info button clicked");
    }

});