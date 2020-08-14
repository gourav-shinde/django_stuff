function submitForm(e) {
    e.preventDefault();
    let name = document.forms["welcome_form"]["name"].value;
    let quiz = document.forms["welcome_form"]["quiz"].value;
  
    sessionStorage.setItem("name", name);

  }