// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Sticky header
window.addEventListener('scroll', function() {
    const header = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    } else {
        header.style.boxShadow = 'none';
    }
});

// Initialize Bootstrap components
var scrollSpy = new bootstrap.ScrollSpy(document.body, {
    target: '#navbarNav'
});

// Animation on scroll
window.addEventListener('scroll', function() {
    const features = document.querySelectorAll('.feature-card');
    features.forEach(feature => {
        const position = feature.getBoundingClientRect();
        if(position.top < window.innerHeight) {
            feature.style.opacity = '1';
        }
    });
});

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', function() {
    const features = document.querySelectorAll('.feature-card');
    features.forEach(feature => {
        feature.style.opacity = '0';
        feature.style.transition = 'opacity 0.5s ease-in';
    });
});

// Typing Effect for Smart Health Monitoring & Prediction System
document.addEventListener('DOMContentLoaded', () => {
    const texts = ['Monitoring', 'Prediction'];
    const element = document.getElementById('typing-effect');
    let index = 0;
    let textIndex = 0;
    
    const typingEffect = () => {
        if (index < texts[textIndex].length) {
            element.textContent += texts[textIndex].charAt(index);
            index++;
            setTimeout(typingEffect, 100);  // Typing speed
        } else {
            setTimeout(() => {
                element.textContent = '';  // Clear the text
                textIndex = (textIndex + 1) % texts.length; // Switch between texts
                index = 0;  // Reset index to start typing new text
                typingEffect(); // Start typing the next text
            }, 1000);  // Delay before starting the next text
        }
    };
    
    typingEffect();  // Start the typing effect
});
