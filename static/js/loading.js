function showLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent scrolling during loading
    }
}

function hideLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'none';
        document.body.style.overflow = 'auto'; // Re-enable scrolling
    }
}

// Optional: Show loading when page is initially loading
document.addEventListener('DOMContentLoaded', function() {
    showLoading();
    window.addEventListener('load', function() {
        setTimeout(hideLoading, 500); // Hide after page fully loads
    });
});