  // FORM DROPDOWN

  document.querySelectorAll('.dropdown-wrapper').forEach((wrapper) => {
    wrapper.addEventListener('click', (e) => {
      e.stopPropagation();
      const dropdown = wrapper.nextElementSibling;
      const isVisible = dropdown.style.display === 'block';

      document.querySelectorAll('.dropdown-options').forEach((options) => {
        options.style.display = 'none';
      });

      dropdown.style.display = isVisible ? 'none' : 'block';
    });
  });

  document.querySelectorAll('.dropdown-option').forEach((option) => {
    option.addEventListener('click', (e) => {
      const input = option.closest('.form-group').querySelector('#form-input');
      input.value = option.textContent.trim();
      option.closest('.dropdown-options').style.display = 'none';


      document.querySelectorAll('.dropdown-option-icon').forEach((icon) => {
        icon.style.display = 'none';
      });


      const icon = option.querySelector('.dropdown-option-icon');
      if (icon) {
        icon.style.display = 'block';
      }
    });
  });

  document.body.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-options').forEach((dropdown) => {
      dropdown.style.display = 'none';
    });
  });

  document.querySelectorAll('.dropdown-wrapper').forEach((wrapper) => {
    wrapper.addEventListener('click', (e) => {
      e.stopPropagation();
    });
  });






   // ADMIN PAGE books dropdown
const dropdownWrapper = document.querySelector('.books-dropdown-wrapper');
const dropdownInput = document.querySelector('#books-input');
const dropdownOptions = document.querySelector('.books-dropdown-options');
const dropdownOptionItems = document.querySelectorAll('.books-dropdown-option');


dropdownWrapper.addEventListener('click', () => {
  dropdownOptions.style.display = dropdownOptions.style.display === 'block' ? 'none' : 'block';
});


dropdownOptionItems.forEach(option => {
  option.addEventListener('click', () => {
    dropdownInput.value = option.textContent;
    dropdownOptions.style.display = 'none';
  });
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('.books-group')) {
    dropdownOptions.style.display = 'none';
  }
});





