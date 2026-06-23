// Utility functions for the bank website

/**
 * Format a number as currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

/**
 * Format a date to French format
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
}

/**
 * Validate IBAN format
 */
function validateIBAN(iban) {
    const ibanRegex = /^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$/;
    return ibanRegex.test(iban);
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

/**
 * Disable/Enable button
 */
function setButtonDisabled(buttonSelector, disabled) {
    const button = document.querySelector(buttonSelector);
    if (button) {
        button.disabled = disabled;
        button.style.opacity = disabled ? '0.5' : '1';
    }
}

/**
 * Check if user is authenticated by checking for session
 */
async function checkAuthentication() {
    try {
        const response = await fetch('/api/user/profile');
        return response.status === 200;
    } catch (error) {
        return false;
    }
}

/**
 * Format account number for display
 */
function formatAccountNumber(account) {
    if (!account) return '';
    return account.substring(0, 4) + ' ' + 
           account.substring(4, 8) + ' ' + 
           account.substring(8, 12) + ' ' + 
           account.substring(12, 16) + ' ' + 
           account.substring(16);
}

/**
 * Calculate transaction fee
 */
function calculateFee(amount) {
    if (amount < 500) return 0;
    if (amount < 2000) return amount * 0.01; // 1%
    return amount * 0.005; // 0.5%
}
