// This file contains JavaScript code that handles the animation logic for the logo falling and stopping, as well as the menu sliding in from the right.

document.addEventListener("DOMContentLoaded", function() {
    const logo = document.querySelector('.logo img');
    const menu = document.querySelector('nav');

    // Start the logo falling animation
    logo.style.animation = 'fall 1s forwards';

    // After the logo animation ends, slide in the menu
    logo.addEventListener('animationend', function() {
        menu.style.animation = 'slideIn 0.5s forwards';
    });
});