// Main JavaScript for Liturgia Católica
// Handles dynamic interactions and UI enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize date picker if present
    initializeDatePicker();
    
    // Initialize PDF preview
    initializePDFPreview();
    
    // Add smooth scroll behavior
    addSmoothScroll();
    
    // Initialize form validation
    initializeFormValidation();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize date picker functionality
 */
function initializeDatePicker() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    
    dateInputs.forEach(input => {
        // Set max date to today + 1 year
        const maxDate = new Date();
        maxDate.setFullYear(maxDate.getFullYear() + 1);
        input.max = maxDate.toISOString().split('T')[0];
        
        // Set min date to 1 year ago
        const minDate = new Date();
        minDate.setFullYear(minDate.getFullYear() - 1);
        input.min = minDate.toISOString().split('T')[0];
    });
}

/**
 * Initialize PDF preview functionality
 */
function initializePDFPreview() {
    const pdfForm = document.getElementById('pdf-customization-form');
    if (!pdfForm) return;
    
    // Listen for changes in form inputs
    const formInputs = pdfForm.querySelectorAll('input, select, textarea');
    formInputs.forEach(input => {
        input.addEventListener('change', updatePreview);
    });
}

/**
 * Update PDF preview based on form values
 */
function updatePreview() {
    const previewArea = document.getElementById('pdf-preview');
    if (!previewArea) return;
    
    const fontSize = document.getElementById('font_size')?.value || 12;
    const fontFamily = document.getElementById('font_family')?.value || 'Times New Roman';
    const liturgicalColor = document.getElementById('liturgical_color')?.value || 'verde';
    
    // Update preview styles
    previewArea.style.fontSize = fontSize + 'px';
    previewArea.style.fontFamily = getFontFamilyName(fontFamily);
    
    // Update color indicator
    updateColorIndicator(liturgicalColor);
}

/**
 * Get font family name from PDF font name
 */
function getFontFamilyName(pdfFont) {
    const fontMap = {
        'Times-Roman': 'Times New Roman, serif',
        'Helvetica': 'Helvetica, Arial, sans-serif',
        'Courier': 'Courier New, monospace'
    };
    return fontMap[pdfFont] || 'Times New Roman, serif';
}

/**
 * Update liturgical color indicator
 */
function updateColorIndicator(color) {
    const indicator = document.getElementById('color-indicator');
    if (!indicator) return;
    
    const colors = {
        'branco': '#ffffff',
        'vermelho': '#c41e3a',
        'verde': '#2d5016',
        'roxo': '#6c2e91',
        'dourado': '#d4af37',
        'preto': '#1a1a1a'
    };
    
    indicator.style.backgroundColor = colors[color] || colors['verde'];
}

/**
 * Add smooth scrolling to anchor links
 */
function addSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Navigate to a specific date
 */
function navigateToDate(dateString) {
    const currentPath = window.location.pathname;
    const basePath = currentPath.split('/').slice(0, -1).join('/');
    window.location.href = `${basePath}/${dateString}`;
}

/**
 * Go to today's liturgy
 */
function goToToday() {
    const today = new Date().toISOString().split('T')[0];
    navigateToDate(today);
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Texto copiado para a área de transferência!', 'success');
    }).catch(err => {
        console.error('Erro ao copiar texto:', err);
        showNotification('Erro ao copiar texto.', 'error');
    });
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

/**
 * Print current page
 */
function printPage() {
    window.print();
}

/**
 * Export liturgy as text
 */
function exportAsText() {
    const content = document.querySelector('.reading-section')?.innerText || '';
    if (!content) {
        showNotification('Nenhum conteúdo para exportar.', 'warning');
        return;
    }
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `liturgia_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Liturgia exportada com sucesso!', 'success');
}

/**
 * Load liturgy for specific date via API
 */
async function loadLiturgyForDate(date) {
    try {
        const response = await fetch(`/api/liturgy/${date}`);
        const data = await response.json();
        
        if (data.success) {
            updateLiturgyDisplay(data);
        } else {
            showNotification('Erro ao carregar liturgia: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error loading liturgy:', error);
        showNotification('Erro ao carregar liturgia.', 'error');
    }
}

/**
 * Update liturgy display with API data
 */
function updateLiturgyDisplay(data) {
    // Update celebration name
    const celebrationElement = document.getElementById('celebration-name');
    if (celebrationElement) {
        celebrationElement.textContent = data.celebration;
    }
    
    // Update liturgical color
    const colorElement = document.getElementById('liturgical-color');
    if (colorElement) {
        colorElement.className = `color-badge ${data.color}`;
        colorElement.textContent = data.color;
    }
    
    // Update readings references
    if (data.readings) {
        ['first', 'psalm', 'second', 'gospel'].forEach(reading => {
            const element = document.getElementById(`reading-${reading}`);
            if (element && data.readings[reading]) {
                element.textContent = data.readings[reading];
            }
        });
    }
}

// Make functions available globally
window.navigateToDate = navigateToDate;
window.goToToday = goToToday;
window.copyToClipboard = copyToClipboard;
window.printPage = printPage;
window.exportAsText = exportAsText;
window.loadLiturgyForDate = loadLiturgyForDate;
