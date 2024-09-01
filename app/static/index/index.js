document.addEventListener("DOMContentLoaded", () => {
  initializeModals();
  initNavbarBurgers();
  initAgreeToTerms();
  initPasswordToggle();
});

// Initialize password visibility toggle
function initPasswordToggle() {
  const passwordId = "password";
  const toggleBtn = document.getElementById(`show-${passwordId}`);

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () =>
      togglePasswordVisibility(passwordId),
    );
  }
}

// Toggle password visibility
function togglePasswordVisibility(inputId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(`${inputId}-icon`);
  const isPassword = input.type === "password";

  input.type = isPassword ? "text" : "password";
  icon.classList.replace(
    `fa-eye${isPassword ? "" : "-slash"}`,
    `fa-eye${isPassword ? "-slash" : ""}`,
  );
}

// Initialize checkbox terms and conditions
function initAgreeToTerms() {
  const agreeButton = document.getElementById("agree-to-terms");
  const termsCheckbox = document.querySelector("#terms-checkbox input");

  if (agreeButton && termsCheckbox) {
    agreeButton.addEventListener("click", () => {
      termsCheckbox.checked = true;
    });
  }
}

// Initialize navbar burger functionality
function initNavbarBurgers() {
  document.querySelectorAll(".navbar-burger").forEach((burger) => {
    burger.addEventListener("click", (event) => {
      const targetId = event.currentTarget.dataset.target;
      const targetElement = document.getElementById(targetId);
      if (targetElement) {
        event.currentTarget.classList.toggle("is-active");
        targetElement.classList.toggle("is-active");
      }
    });
  });
}

// Modal functionality
function initializeModals() {
  initializeModalTriggers();
  initializeModalClosers();
  initializeKeyboardEvents();
}

function initializeModalTriggers() {
  document.querySelectorAll(".js-modal-trigger").forEach(($trigger) => {
    const $target = document.getElementById($trigger.dataset.target);
    $trigger.addEventListener("click", () => openModal($target));
  });
}

function initializeModalClosers() {
  document
    .querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button",
    )
    .forEach(($close) => {
      const $target = $close.closest(".modal");
      $close.addEventListener("click", () => closeModal($target));
    });
}

function initializeKeyboardEvents() {
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeAllModals();
  });
}

function openModal($el) {
  $el.classList.add("is-active");
}

function closeModal($el) {
  $el.classList.remove("is-active");
}

function closeAllModals() {
  document.querySelectorAll(".modal").forEach(closeModal);
}
