document.addEventListener('DOMContentLoaded', () => {
    // Animate progress bars on initial load
    document.querySelectorAll('.progress-fill').forEach(progressBar => {
        const targetWidth = progressBar.style.width;
        progressBar.style.width = '0';
        setTimeout(() => {
            progressBar.style.width = targetWidth;
        }, 500);
    });

    // Add hover effects to cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.boxShadow = '0 8px 12px -2px rgba(0, 0, 0, 0.2)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        });
    });

    // Add animation to table rows
    document.querySelectorAll('.activities-table tr').forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'translateX(10px)';
            row.style.transition = 'transform 0.3s ease';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.transform = 'translateX(0)';
        });
    });
});

// Real-time clock function
function updateLiveClock() {
    const clockElement = document.createElement('div');
    clockElement.id = 'live-clock';
    clockElement.style.position = 'fixed';
    clockElement.style.bottom = '20px';
    clockElement.style.right = '20px';
    clockElement.style.background = 'var(--card-bg)';
    clockElement.style.padding = '10px 20px';
    clockElement.style.borderRadius = '8px';
    clockElement.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
    document.body.appendChild(clockElement);

    setInterval(() => {
        const now = new Date();
        clockElement.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }, 1000);
}

updateLiveClock();