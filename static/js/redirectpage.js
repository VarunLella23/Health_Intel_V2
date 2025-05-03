const bodySystems = [
    {
        name: 'Heart',
        icon: '<i class="fas fa-heartbeat"></i>',
        diseases: [
            { name: 'Heart Failure', path: '/heart' },
            { name: 'Coronary Artery Disease', path: 'heart-cad.html' },
            { name: 'Arrhythmia', path: 'heart-arrhythmia.html' }
        ]
    },
    {
        name: 'Lungs',
        icon: '<i class="fas fa-lungs"></i>',
        diseases: [
            { name: 'Lung Cancer', path: '/lungs' },
            { name: 'COPD', path: 'lungs-copd.html' },
            { name: 'Asthma', path: 'lungs-asthma.html' }
        ]
    },
    {
        name: 'Liver',
        icon: '<i class="fas fa-bacteria"></i>',
        diseases: [
            { name: 'Liver Cancer', path: '/liver' },
            { name: 'Cirrhosis', path: 'liver-cirrhosis.html' },
            { name: 'Fatty Liver', path: 'liver-fatty.html' }
        ]
    },
    {
        name: 'Brain',
        icon: '<i class="fas fa-brain"></i>',
        diseases: [
            { name: 'Mental Health', path: '/mental-health' },
            { name: 'Epilepsy', path: 'brain-epilepsy.html' },
            { name: 'Stroke', path: 'brain-stroke.html' }
        ]
    },
    {
        name: 'Kidneys',
        icon: '<i class="fas fa-filter"></i>',
        diseases: [
            { name: 'Kidney Stones', path: 'kidney-stones.html' },
            { name: 'CKD', path: 'kidney-ckd.html' },
            { name: 'UTI', path: 'kidney-uti.html' }
        ]
    },
    {
        name: 'Pancreas',
        icon: '<i class="fas fa-procedures"></i>',
        diseases: [
            { name: 'Diabetes', path: '/diabetes' },
            { name: 'CKD', path: 'kidney-ckd.html' },
            { name: 'UTI', path: 'kidney-uti.html' }
        ]
    },
    {
        name: 'Skin',
        icon: '<i class="fas fa-hand-sparkles"></i>',
        diseases: [
            { name: 'Eczema', path: 'skin-eczema.html' },
            { name: 'Psoriasis', path: 'skin-psoriasis.html' },
            { name: 'Acne', path: 'skin-acne.html' }
        ]
    }
];

const bodyGrid = document.getElementById('bodyGrid');
const searchInput = document.getElementById('searchInput');

function highlightMatch(text, searchTerm) {
    if (!searchTerm) return text;
    const regex = new RegExp(searchTerm, 'gi');
    return text.replace(regex, match => `<span class="highlight">${match}</span>`);
}

function createCard(system, searchTerm = '') {
    const card = document.createElement('div');
    card.className = 'health-card';
    
    const header = document.createElement('div');
    header.className = 'card-header';
    header.innerHTML = `
    <div class="card-icon">${system.icon}</div>
    <div class="card-title">${highlightMatch(system.name, searchTerm)}</div>
    <div class="expand-indicator">
        <span class="expand-text"></span>
        <i class="fas fa-chevron-down chevron-icon"></i>
    </div>
`;

    const diseaseList = document.createElement('div');
    diseaseList.className = 'disease-list';
    
    system.diseases.forEach(disease => {
        if (searchTerm && !disease.name.toLowerCase().includes(searchTerm)) return;
        
        const diseaseItem = document.createElement('div');
        diseaseItem.className = 'disease-item';
        diseaseItem.innerHTML = `
            <div class="disease-name">${highlightMatch(disease.name, searchTerm)}</div>
            <a href="${disease.path}" class="disease-link">View</a>
        `;
        diseaseList.appendChild(diseaseItem);
    });

    card.appendChild(header);
    card.appendChild(diseaseList);

    if (searchTerm) {
        diseaseList.classList.add('expanded');
    }

    header.addEventListener('click', () => {
        diseaseList.classList.toggle('expanded');
    });

    return card;
}

function renderCards(searchTerm = '') {
    bodyGrid.innerHTML = '';
    const term = searchTerm.toLowerCase().trim();

    if (!term) {
        // Show all systems with collapsed lists
        bodySystems.forEach(system => {
            bodyGrid.appendChild(createCard(system));
        });
    } else {
        // Show filtered results
        bodySystems.forEach(system => {
            const hasSystemMatch = system.name.toLowerCase().includes(term);
            const hasDiseaseMatch = system.diseases.some(d => d.name.toLowerCase().includes(term));
            
            if (hasSystemMatch || hasDiseaseMatch) {
                const card = createCard(system, term);
                bodyGrid.appendChild(card);
            }
        });
    }
}

// Event listeners
searchInput.addEventListener('input', (e) => {
    renderCards(e.target.value);
});

document.addEventListener('DOMContentLoaded', () => {
    renderCards();
    bodyGrid.style.opacity = '1';
});

// Initialize with fade-in effect
bodyGrid.style.opacity = '0';
bodyGrid.style.transition = 'opacity 0.3s ease';




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

header.addEventListener('click', () => {
    // Toggle current card
    card.classList.toggle('expanded');
    diseaseList.classList.toggle('expanded');
    
    // Collapse other cards
    document.querySelectorAll('.health-card').forEach(otherCard => {
        if (otherCard !== card) {
            otherCard.classList.remove('expanded');
            otherCard.querySelector('.disease-list').classList.remove('expanded');
        }
    });
});