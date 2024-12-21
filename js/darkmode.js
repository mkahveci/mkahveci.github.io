function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');

  // Store the user's preference in localStorage
  if (body.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }
}

// Check user's preference on page load
const darkMode = localStorage.getItem('darkMode');
if (darkMode === 'disabled') { // Check if dark mode is explicitly disabled
  document.body.classList.remove('dark-mode');
} else {
  document.body.classList.add('dark-mode'); // Enable dark mode by default
}

// Add an event listener to a button or link to toggle dark mode
const darkModeToggle = document.getElementById('dark-mode-toggle'); // Replace with your button/link ID
if (darkModeToggle) {
  darkModeToggle.addEventListener('click', toggleDarkMode);
}