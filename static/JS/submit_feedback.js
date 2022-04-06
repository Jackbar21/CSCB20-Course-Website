var form = document.getElementById("form");

if (form) {
    form.addEventListener('submit', (e) => {
    e.preventDefault();
    console.log('Thank you for your feedback!');
    });
  }
