document.addEventListener('DOMContentLoaded', (event) => {
    ((localStorage.getItem('mode') || 'light') === 'dark') ? document.querySelector('body').classList.add('dark') : document.querySelector('body').classList.remove('dark')})
