// static/script.js (Versión Completa y Funcional)

document.addEventListener('DOMContentLoaded', () => {
    // --- Lógica para el menú de perfil en el header ---
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

    // --- Lógica específica para la página de registro ---
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) {
        // Si no encontramos el formulario de registro, no hacemos nada más.
        return; 
    }

    // Si estamos en la página de registro, obtenemos todos los elementos necesarios.
    const roleSelectionStep = document.getElementById('roleSelectionStep');
    const roleButtons = document.querySelectorAll('.role-btn');
    const userRoleInput = document.getElementById('id_user_role');
    const providerFields = document.getElementById('providerFields');
    const changeRoleBtn = document.getElementById('changeRoleBtn');
    const submitButton = document.getElementById('submit-btn-js');

    // Función para mostrar el formulario
    const selectRoleAndShowForm = (selectedRole) => {
        userRoleInput.value = selectedRole;
        roleButtons.forEach(btn => {
            btn.classList.toggle('border-brand-primary', btn.dataset.role === selectedRole);
            btn.classList.toggle('bg-brand-primary/5', btn.dataset.role === selectedRole);
        });
        providerFields.classList.toggle('hidden', selectedRole !== 'service_provider');
        roleSelectionStep.classList.add('hidden');
        registerForm.classList.remove('hidden');
    };

    // Función para volver a la selección de rol
    const goBackToRoleSelection = () => {
        registerForm.classList.add('hidden');
        roleSelectionStep.classList.remove('hidden');
        userRoleInput.value = '';
        roleButtons.forEach(btn => btn.classList.remove('border-brand-primary', 'bg-brand-primary/5'));
    };
    
    // Asignación de eventos a los botones de control
    roleButtons.forEach(button => button.addEventListener('click', () => selectRoleAndShowForm(button.dataset.role)));
    if (changeRoleBtn) {
        changeRoleBtn.addEventListener('click', goBackToRoleSelection);
    }
    
    // Restaurar el rol si la página se recargó con un error del servidor
    const initialRole = document.body.dataset.initialRole;
    if (initialRole) {
        selectRoleAndShowForm(initialRole);
    }

    // === EL CORAZÓN DE LA SOLUCIÓN: MANEJO DEL ENVÍO DEL FORMULARIO ===
    submitButton.addEventListener('click', () => {
        // No necesitamos event.preventDefault() porque el botón ya no tiene acción por defecto.
        
        // 1. Validamos del lado del cliente
        if (validateClientSide()) {
            // 2. Si es válido, enviamos con AJAX
            submitFormWithAjax();
        } else {
            console.error("Errores de validación del cliente. El envío se ha detenido.");
        }
    });

    const submitFormWithAjax = () => {
        submitButton.disabled = true;
        submitButton.textContent = 'Verificando...';

        const formData = new FormData(registerForm);
        const url = registerForm.action;

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.redirect_url;
            } else if (data.status === 'error') {
                displayServerErrors(data.errors);
            }
        })
        .catch(error => console.error('Error en la petición AJAX:', error))
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Registrarme';
        });
    };
    
    function displayServerErrors(errors) {
        // Limpia cualquier error de cliente previo
        clearAllErrors();
        
        for (const fieldName in errors) {
            const errorMessages = errors[fieldName]; // Es una lista de errores
            const firstError = errorMessages[0].message;
            const fieldId = `id_${fieldName}`;
            showError(fieldId, firstError);
        }
    }

    function validateClientSide() {
        let isValid = true;
        clearAllErrors(); // Limpia errores antes de validar de nuevo

        // Validaciones individuales
        if (!validateRequired('id_first_name', 'El nombre es obligatorio.')) isValid = false;
        if (!validateRequired('id_last_name', 'El apellido es obligatorio.')) isValid = false;
        if (!validateRequired('id_user_address', 'La dirección es obligatoria.')) isValid = false;
        if (!validateBirthdate('id_user_birthdate')) isValid = false;
        if (!validatePhone('id_user_phone')) isValid = false;
        if (!validateEmail('id_email')) isValid = false;
        if (!validateFile('id_user_picture', 'Debes subir una foto de perfil.')) isValid = false;
        if (!validatePasswords('id_password1', 'id_password2')) isValid = false;
        
        // Valida la descripción solo si el rol es 'provider'
        if (userRoleInput.value === 'service_provider') {
            if (!validateRequired('id_description', 'La descripción es obligatoria para proveedores.')) isValid = false;
        }

        return isValid;
    }

    // Funciones auxiliares para mostrar/limpiar errores
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

        if (!pass1 || pass1.value.length < 8) {
            showError(pass1Id, 'La contraseña debe tener al menos 8 caracteres.');
            isValid = false;
        }
        if (!pass2 || pass1.value !== pass2.value) {
            showError(pass2Id, 'Las contraseñas no coinciden.');
            isValid = false;
        }
        return isValid;
    }
});