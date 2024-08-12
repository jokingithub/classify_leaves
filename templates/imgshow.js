// imgshow.js

let currentIndex = 0;
const images = document.querySelectorAll('.carousel img');
const totalImages = images.length;

function showNextImage() {
    // Hide the current image
    images[currentIndex].classList.add('hidden');

    // Calculate the next image index
    currentIndex = (currentIndex + 1) % totalImages;

    // Show the next image
    images[currentIndex].classList.remove('hidden');
}

function showPreviousImage() {
    // Hide the current image
    images[currentIndex].classList.add('hidden');

    // Calculate the previous image index
    currentIndex = (currentIndex - 1 + totalImages) % totalImages;

    // Show the previous image
    images[currentIndex].classList.remove('hidden');
}

// Set interval to change image every 3 seconds
setInterval(showNextImage, 3500);

// Optional: Add event listeners for navigation buttons (if any)
// document.querySelector('.next-button').addEventListener('click', showNextImage);
// document.querySelector('.prev-button').addEventListener('click', showPreviousImage);
