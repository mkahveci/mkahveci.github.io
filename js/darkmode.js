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
if (darkMode === 'enabled') {
  document.body.classList.add('dark-mode');
}

// Add an event listener to a button or link to toggle dark mode
const darkModeToggle = document.getElementById('dark-mode-toggle'); // Replace with your button/link ID
if (darkModeToggle) {
  darkModeToggle.addEventListener('click', toggleDarkMode);
}