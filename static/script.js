document.addEventListener('DOMContentLoaded', function() {
    const profileMenuBtn = document.getElementById('profile-menu-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileMenuBtn && profileDropdown) {
        profileMenuBtn.addEventListener('click', (event) => {
            event.stopPropagation();
            profileDropdown.classList.toggle('hidden');
        });
        window.addEventListener('click', () => {
            if (!profileDropdown.classList.contains('hidden')) {
                profileDropdown.classList.add('hidden');
            }
        });
        profileDropdown.addEventListener('click', (event) => {
            event.stopPropagation();
        });
    }
  const roleButtons = document.querySelectorAll('.role-btn');
  const roleSelectionStep = document.getElementById('roleSelectionStep');
  const registerForm = document.getElementById('registerForm');
  const userRoleInput = document.querySelector('input[name="user_role"]');
  const changeRoleBtn = document.getElementById('changeRoleBtn');
  const providerFields = document.getElementById('providerFields');
  const submitButton = document.getElementById('submit-btn-js');

  // Selección de rol
  roleButtons.forEach(button => {
    button.addEventListener('click', function() {
      const selectedRole = this.getAttribute('data-role');
      userRoleInput.value = selectedRole;
      
      roleSelectionStep.classList.add('hidden');
      registerForm.classList.remove('hidden');
      
      if (selectedRole === 'service_provider') {
        providerFields.classList.remove('hidden');
      } else {
        providerFields.classList.add('hidden');
      }
    });
  });

  // Cambiar rol
  changeRoleBtn.addEventListener('click', function() {
    registerForm.classList.add('hidden');
    roleSelectionStep.classList.remove('hidden');
    providerFields.classList.add('hidden');
  });

  // ============ MANEJO DEL SUBMIT CON AJAX ============
  submitButton.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Validación del lado del cliente
    if (validateClientSide()) {
      submitFormWithAjax();
    }
  });

  function submitFormWithAjax() {
    submitButton.disabled = true;
    submitButton.textContent = 'Creando cuenta...';

    const formData = new FormData(registerForm);

    fetch(registerForm.action || window.location.href, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        window.location.href = data.redirect_url;
      } else if (data.status === 'error') {
        displayServerErrors(data.errors);
      }
    })
    .catch(error => {
      console.error('Error en la petición:', error);
      alert('Ocurrió un error al crear la cuenta. Por favor, intenta nuevamente.');
    })
    .finally(() => {
      submitButton.disabled = false;
      submitButton.textContent = 'Crear mi cuenta';
    });
  }

  function displayServerErrors(errors) {
    clearAllErrors();
    
    for (const fieldName in errors) {
      const errorMessages = errors[fieldName];
      const firstError = errorMessages[0].message;
      const fieldId = `id_${fieldName}`;
      showError(fieldId, firstError);
    }
  }

  function validateClientSide() {
    let isValid = true;
    clearAllErrors();

    if (!validateRequired('id_first_name', 'El nombre es obligatorio.')) isValid = false;
    if (!validateRequired('id_last_name', 'El apellido es obligatorio.')) isValid = false;
    if (!validateRequired('id_user_address', 'La dirección es obligatoria.')) isValid = false;
    if (!validateBirthdate('id_user_birthdate')) isValid = false;
    if (!validatePhone('id_user_phone')) isValid = false;
    if (!validateEmail('id_email')) isValid = false;
    if (!validateFile('id_user_picture', 'Debes subir una foto de perfil.')) isValid = false;
    if (!validatePasswords('id_password1', 'id_password2')) isValid = false;
    
    if (userRoleInput.value === 'service_provider') {
      if (!validateRequired('id_description', 'La descripción es obligatoria para proveedores.')) isValid = false;
    }

    return isValid;
  }

  function showError(fieldId, message) {
    const errorElement = document.getElementById(`${fieldId}-error`);
    if (errorElement) {
      errorElement.textContent = message;
      errorElement.classList.remove('hidden');
    }
  }

  function clearAllErrors() {
    document.querySelectorAll('p[id$="-error"]').forEach(p => {
      p.textContent = '';
      p.classList.add('hidden');
    });
  }

  function validateRequired(fieldId, message) {
    const input = document.getElementById(fieldId);
    if (!input || input.value.trim() === '') {
      showError(fieldId, message);
      return false;
    }
    return true;
  }

  function validateFile(fieldId, message) {
    const input = document.getElementById(fieldId);
    if (!input || input.files.length === 0) {
      showError(fieldId, message);
      return false;
    }
    
    const file = input.files[0];
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      showError(fieldId, 'Por favor, sube un archivo de imagen válido (JPG, PNG, GIF, WEBP).');
      return false;
    }
    
    return true;
  }
  
  function validateBirthdate(fieldId) {
    const input = document.getElementById(fieldId);
    if (!input || !input.value) {
      showError(fieldId, 'Debes seleccionar tu fecha de nacimiento.');
      return false;
    }
    const birthdate = new Date(input.value);
    const age = (new Date() - birthdate) / (1000 * 60 * 60 * 24 * 365.25);
    if (age < 18) {
      showError(fieldId, 'Debes ser mayor de 18 años para registrarte.');
      return false;
    }
    if (age > 100) {
      showError(fieldId, 'Por favor, ingresa una fecha de nacimiento válida.');
      return false;
    }
    return true;
  }

  function validatePhone(fieldId) {
    const input = document.getElementById(fieldId);
    if (!input || !/^\d{7,15}$/.test(input.value)) {
      showError(fieldId, 'Debe ser un número válido de 7 a 15 dígitos.');
      return false;
    }
    return true;
  }

  function validateEmail(fieldId) {
    const input = document.getElementById(fieldId);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!input || !emailRegex.test(input.value)) {
      showError(fieldId, 'Por favor, ingresa un correo electrónico válido.');
      return false;
    }
    return true;
  }

  function validatePasswords(pass1Id, pass2Id) {
    const pass1 = document.getElementById(pass1Id);
    const pass2 = document.getElementById(pass2Id);
    let isValid = true;

    // Validar longitud mínima
    if (!pass1 || pass1.value.length < 8) {
      showError(pass1Id, 'La contraseña debe tener al menos 8 caracteres.');
      isValid = false;
    }
    
    // Validar que no sea completamente numérica
    else if (/^\d+$/.test(pass1.value)) {
      showError(pass1Id, 'La contraseña no puede ser completamente numérica.');
      isValid = false;
    }
    
    // Validar contraseñas comunes
    else if (isCommonPassword(pass1.value)) {
      showError(pass1Id, 'Esta contraseña es demasiado común. Por favor elige una más segura.');
      isValid = false;
    }
    
    // Validar que contenga letras y números
    else if (!(/[a-zA-Z]/.test(pass1.value) && /\d/.test(pass1.value))) {
      showError(pass1Id, 'La contraseña debe contener letras y números.');
      isValid = false;
    }
    
    // Validar que las contraseñas coincidan
    if (!pass2 || pass1.value !== pass2.value) {
      showError(pass2Id, 'Las contraseñas no coinciden.');
      isValid = false;
    }
    
    return isValid;
  }
  
  function isCommonPassword(password) {
    const commonPasswords = [
      'password', '12345678', '123456789', 'qwerty', 'abc123', 
      'password1', '12345', '1234567', 'welcome', 'monkey',
      'letmein', 'dragon', 'baseball', 'iloveyou', 'trustno1',
      'sunshine', 'master', 'admin', 'password123', '111111'
    ];
    return commonPasswords.includes(password.toLowerCase());
  }
});