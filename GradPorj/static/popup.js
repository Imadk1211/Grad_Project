function openPopup() {
    document.querySelector('.popup').style.display = 'block';
}

function closePopup() {
    document.querySelector('.popup').style.display = 'none';
}

document.getElementById('uploadButton').addEventListener('click', function() {
    openPopup();
});

// Handle form submission
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    // Handle file upload here
    closePopup(); // Close the popup after submission
});
