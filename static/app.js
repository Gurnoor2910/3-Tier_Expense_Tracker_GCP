// Theme toggle button logic
const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
  if (document.body.classList.contains('theme-light')) {
    document.body.classList.remove('theme-light');
    themeToggle.textContent = '🌙';
  } else {
    document.body.classList.add('theme-light');
    themeToggle.textContent = '☀️';
  }
});

// Drawer open/close logic
const drawer = document.getElementById('drawer');
const addBtn = document.getElementById('addBtn');
const closeDrawerBtn = document.getElementById('closeDrawer');

if (addBtn && drawer) {
  addBtn.addEventListener('click', () => {
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
  });
}

if (closeDrawerBtn && drawer) {
  closeDrawerBtn.addEventListener('click', () => {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
  });
}
