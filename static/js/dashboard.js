class Dashboard {
    constructor() {
      this.initialize();
    }
  
    initialize() {
      this.setupEventListeners();
      this.animateElements();
      this.initializeClock();
      this.observePerformance();
    }
  
    setupEventListeners() {
      // Use event delegation for better performance
      document.body.addEventListener('mouseover', this.handleHover.bind(this));
    }
  
    animateElements() {
      const animateProgressBar = (element) => {
        const targetWidth = element.dataset.width;
        element.style.width = '0';
        requestAnimationFrame(() => {
          element.style.width = targetWidth;
        });
      };
  
      document.querySelectorAll('.progress-fill').forEach(animateProgressBar);
    }
  
    handleHover(event) {
      const card = event.target.closest('.card');
      if (card) {
        card.classList.toggle('hover-state', event.type === 'mouseenter');
      }
    }
  
    initializeClock() {
      const clock = document.createElement('div');
      clock.id = 'live-clock';
      document.body.appendChild(clock);
      
      this.updateClock();
      setInterval(this.updateClock.bind(this), 1000);
    }
  
    updateClock() {
      const options = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      };
      document.getElementById('live-clock').textContent = 
        new Date().toLocaleTimeString('en-US', options);
    }
  
    observePerformance() {
      if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            console.log('[Performance]', entry.name, entry.duration);
          }
        });
        observer.observe({ entryTypes: ['measure', 'resource'] });
      }
    }
  }
  
  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
    // Remove loading state
    document.querySelector('.loading-overlay').remove();
  });
  
  // Register service worker
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js');
    });
  }