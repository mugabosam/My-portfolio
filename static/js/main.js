// Dark Mode Toggle with LocalStorage and System Preference
document.addEventListener('DOMContentLoaded', () => {
    // Initialize dark mode
    const isDarkMode = localStorage.getItem('darkMode') === 'true' ||
                      (!('darkMode' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches);
    document.documentElement.classList.toggle('dark', isDarkMode);
    localStorage.setItem('darkMode', isDarkMode);

    // Add transition after initial load
    setTimeout(() => {
        document.documentElement.classList.add('transition-colors');
        document.documentElement.style.transitionDuration = '300ms';
    }, 100);
});

document.getElementById('dark-mode-toggle').addEventListener('click', function() {
    const isDark = document.documentElement.classList.toggle('dark');

    // Store preference
    localStorage.setItem('darkMode', isDark);
    document.cookie = `dark_mode=${isDark}; path=/; max-age=${60 * 60 * 24 * 365}`; // 1 year

    // Add rotation animation
    const icon = this.querySelector('i');
    icon.classList.add('rotate-180', 'transition-transform');
    setTimeout(() => icon.classList.remove('rotate-180'), 500);
});

// Enhanced Contact Form Submission
document.getElementById('contact-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
        <span class="inline-block animate-spin">
            <i class="fas fa-spinner"></i>
        </span> Sending...
    `;

    try {
        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            },
        });

        const data = await response.json();

        if (!response.ok) throw new Error('Server error');
        if (data.success) {
            showNotification('Message sent successfully!', 'success');
            form.reset();
        } else {
            handleFormErrors(data.errors);
        }
    } catch (error) {
        showNotification('Failed to send message. Please try again later.', 'error');
        console.error('Form submission error:', error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
    }
});

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-6 right-6 px-6 py-3 rounded-lg shadow-lg text-white 
        ${type === 'success' ? 'bg-green-500' : 
         type === 'error' ? 'bg-red-500' : 'bg-blue-500'}
        animate-slide-in`;

    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle'} mr-2"></i>
        ${message}
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('opacity-0', 'translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Form Error Handling
function handleFormErrors(errors) {
    // Clear previous errors
    document.querySelectorAll('.form-error').forEach(el => el.remove());

    for (const [field, messages] of Object.entries(errors)) {
        const input = document.querySelector(`[name=${field}]`);
        if (!input) continue;

        const errorContainer = document.createElement('div');
        errorContainer.className = 'form-error text-red-500 text-sm mt-1';
        errorContainer.innerHTML = messages.join('<br>');

        input.parentNode.insertBefore(errorContainer, input.nextSibling);
        input.classList.add('border-red-500', 'dark:border-red-400');

        input.addEventListener('input', () => {
            input.classList.remove('border-red-500', 'dark:border-red-400');
            errorContainer.remove();
        }, { once: true });
    }
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slide-in {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    .animate-slide-in {
        animation: slide-in 0.3s ease-out;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .animate-spin {
        animation: spin 1s linear infinite;
    }
`;
document.head.appendChild(style);