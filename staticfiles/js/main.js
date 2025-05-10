document.addEventListener('DOMContentLoaded', function() {
    // Sahifa yuklanganda ishga tushadigan kod
    console.log('O\'zbekiston Respublikasi Hukumati portali yuklandi');

    // Xabarlarni avtomatik yopish
    setupAlertDismissal();

    // Formalarni validatsiya qilish
    setupFormValidation();
});

// Xabarlarni avtomatik yopish
function setupAlertDismissal() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 500);
        }, 5000);
    });
}

// Formalarni validatsiya qilish
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const requiredInputs = form.querySelectorAll('input[required], select[required], textarea[required]');

        requiredInputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateInput(input);
            });

            input.addEventListener('input', function() {
                validateInput(input);
            });
        });

        form.addEventListener('submit', function(event) {
            let isValid = true;

            requiredInputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                event.preventDefault();
            }
        });
    });
}

// Input validatsiyasi
function validateInput(input) {
    const value = input.value.trim();
    const errorElement = input.nextElementSibling;

    if (value === '') {
        input.classList.add('is-invalid');
        if (errorElement && errorElement.classList.contains('alert-danger')) {
            errorElement.textContent = 'Bu maydon to\'ldirilishi shart';
        }
        return false;
    } else {
        input.classList.remove('is-invalid');
        if (errorElement && errorElement.classList.contains('alert-danger')) {
            errorElement.textContent = '';
        }
        return true;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Sahifa yuklanganda ishga tushadigan kod
    console.log('O\'zbekiston Respublikasi Hukumati portali yuklandi');

    // Mobil menyu
    setupMobileMenu();

    // Xabarlarni avtomatik yopish
    setupAlertDismissal();

    // Formalarni validatsiya qilish
    setupFormValidation();

    // Rasmni oldindan ko'rish
    setupImagePreview();
});

// Mobil menyu
function setupMobileMenu() {
    const navbarToggle = document.getElementById('navbarToggle');
    const navbarNav = document.getElementById('navbarNav');

    if (navbarToggle && navbarNav) {
        navbarToggle.addEventListener('click', function() {
            navbarNav.classList.toggle('show');
        });

        // Menyu tashqarisiga bosilganda menyuni yopish
        document.addEventListener('click', function(event) {
            if (!navbarToggle.contains(event.target) && !navbarNav.contains(event.target)) {
                navbarNav.classList.remove('show');
            }
        });
    }
}



// Parol kuchliligini tekshirish
function checkPasswordStrength(input) {
    const password = input.value;
    const strengthMeter = document.getElementById('passwordStrength');
    if (!strengthMeter) return;

    // Parol kuchliligi mezonlari
    const hasLowerCase = /[a-z]/.test(password);
    const hasUpperCase = /[A-Z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChars = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const isLongEnough = password.length >= 8;

    // Parol kuchliligini hisoblash (0-100)
    let strength = 0;
    if (hasLowerCase) strength += 20;
    if (hasUpperCase) strength += 20;
    if (hasNumbers) strength += 20;
    if (hasSpecialChars) strength += 20;
    if (isLongEnough) strength += 20;

    // Kuchlilik darajasini ko'rsatish
    strengthMeter.style.width = `${strength}%`;

    if (strength < 40) {
        strengthMeter.className = 'progress-bar bg-danger';
        strengthMeter.textContent = 'Juda zaif';
    } else if (strength < 60) {
        strengthMeter.className = 'progress-bar bg-warning';
        strengthMeter.textContent = 'Zaif';
    } else if (strength < 80) {
        strengthMeter.className = 'progress-bar bg-info';
        strengthMeter.textContent = 'O\'rtacha';
    } else {
        strengthMeter.className = 'progress-bar bg-success';
        strengthMeter.textContent = 'Kuchli';
    }
}

// Rasmni oldindan ko'rish
function setupImagePreview() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');

    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (!file) return;

            // Fayl turi tekshirish
            const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
            if (!validTypes.includes(file.type)) {
                alert('Faqat JPEG, PNG yoki GIF formatidagi rasmlar qabul qilinadi');
                this.value = '';
                return;
            }

            // Fayl hajmini tekshirish (5MB dan katta bo'lmasligi kerak)
            if (file.size > 5 * 1024 * 1024) {
                alert('Rasm hajmi 5MB dan oshmasligi kerak');
                this.value = '';
                return;
            }

            // Rasm preview ko'rsatish
            const previewId = this.dataset.preview || 'imagePreview';
            const preview = document.getElementById(previewId);

            if (preview) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    });
}
