document.addEventListener("DOMContentLoaded", () => {
  const seekerBtn = document.getElementById("seekerBtn");
  const providerBtn = document.getElementById("providerBtn");
  const providerFields = document.getElementById("providerFields");
  const registerForm = document.getElementById("registerForm");

  // OJO: usamos el hidden del form (Django genera id="id_user_role")
  const roleInput = document.getElementById("id_user_role");

  // Input de imagen (forzado a id="id_user_picture")
  const fileInput = document.getElementById("id_user_picture");
  const fileError = document.getElementById("fileError");
  if (fileError) fileError.classList.add("hidden");

  function applyRoleStyles(role) {
    if (role === "service_seeker") {
      providerFields.classList.add("hidden");
      seekerBtn.classList.add("bg-indigo-600", "text-white");
      seekerBtn.classList.remove("bg-gray-200", "text-gray-800");

      providerBtn.classList.remove("bg-indigo-600", "text-white");
      providerBtn.classList.add("bg-gray-200", "text-gray-800");
    } else if (role === "service_provider") {
      providerFields.classList.remove("hidden");
      providerBtn.classList.add("bg-indigo-600", "text-white");
      providerBtn.classList.remove("bg-gray-200", "text-gray-800");

      seekerBtn.classList.remove("bg-indigo-600", "text-white");
      seekerBtn.classList.add("bg-gray-200", "text-gray-800");
    }
  }

  function selectRole(role) {
    if (!registerForm.classList.contains("hidden")) {
      // ok
    } else {
      registerForm.classList.remove("hidden");
    }
    roleInput.value = role;
    applyRoleStyles(role);
  }

  // Clicks de rol
  if (seekerBtn) {
    seekerBtn.addEventListener("click", (e) => {
      e.preventDefault();
      selectRole("service_seeker");
    });
  }

  if (providerBtn) {
    providerBtn.addEventListener("click", (e) => {
      e.preventDefault();
      selectRole("service_provider");
    });
  }

  // Validación previa al submit
  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      // 1) Debe haber rol
      if (!roleInput.value) {
        e.preventDefault();
        alert("Debes seleccionar un tipo de usuario (Buscador u Ofertante).");
        return;
      }
      // 2) Debe haber imagen
      if (!fileInput || !fileInput.files || !fileInput.files.length) {
        e.preventDefault();
        if (fileError) fileError.classList.remove("hidden");
        fileInput?.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      } else {
        if (fileError) fileError.classList.add("hidden");
      }
    });
  }

  // Si el server devolvió el form con rol (POST inválido), re-selecciona para mantener estado
  if (window.__initialSelectedRole) {
    selectRole(window.__initialSelectedRole);
  }
});
