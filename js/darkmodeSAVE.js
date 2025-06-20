function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');

  // Toggle the icon of the dark mode
  const darkModeIcon = document.getElementById('dark-mode-icon');
  if (body.classList.contains('dark-mode')) {
    darkModeIcon.classList.remove('fa-moon');
    darkModeIcon.classList.add('fa-sun');
    darkModeIcon.style.color = '#fff'; // White in dark mode
  } else {
    darkModeIcon.classList.remove('fa-sun');
    darkModeIcon.classList.add('fa-moon');
    darkModeIcon.style.color = '#333'; // Dark gray in light mode
  }

  // Store the user's preference in localStorage
  if (body.classList.contains('dark-mode')) {
    localStorage.setItem('darkMode', 'enabled');
  } else {
    localStorage.setItem('darkMode', 'disabled');
  }
}

// Check user's preference on page load
const darkMode = localStorage.getItem('darkMode');
if (darkMode === 'disabled') {
  document.body.classList.remove('dark-mode');
} else {
  document.body.classList.add('dark-mode');
  const darkModeIcon = document.getElementById('dark-mode-icon');
  darkModeIcon.classList.remove('fa-moon');
  darkModeIcon.classList.add('fa-sun');
  darkModeIcon.style.color = '#fff';
}

// Add an event listener to the toggle to call the function
const darkModeToggle = document.getElementById('dark-mode-toggle');
if (darkModeToggle) {
  darkModeToggle.addEventListener('click', toggleDarkMode);
}