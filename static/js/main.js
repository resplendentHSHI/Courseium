/**
 * Courseium Medical Case Simulation
 * Main JavaScript
 */

// DOM elements
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the simulation page
    const simulationPage = document.querySelector('.simulation-container');
    if (simulationPage) {
        initializeSimulation();
    }

    // Check if we're on the cases page
    const casesPage = document.querySelector('.case-filters');
    if (casesPage) {
        initializeCaseFilters();
    }


});

/**
 * Initialize Simulation Page Functionality
 */
function initializeSimulation() {
    // Audio player functionality
    const playButton = document.getElementById('play-audio');
    if (playButton) {
        const audioElement = document.getElementById('patient-audio');
        
        playButton.addEventListener('click', function() {
            if (audioElement) {
                // Real audio playback
                if (audioElement.paused) {
                    audioElement.play();
                    this.classList.add('playing');
                    
                    // Update waveform appearance during playback
                    const waveform = document.querySelector('.waveform-placeholder');
                    if (waveform) {
                        waveform.style.backgroundSize = '5% 100%';
                    }
                    
                    // Reset when audio ends
                    audioElement.onended = function() {
                        playButton.classList.remove('playing');
                        if (waveform) {
                            waveform.style.backgroundSize = '15% 100%';
                        }
                    };
                } else {
                    audioElement.pause();
                    this.classList.remove('playing');
                    
                    // Reset waveform
                    const waveform = document.querySelector('.waveform-placeholder');
                    if (waveform) {
                        waveform.style.backgroundSize = '15% 100%';
                    }
                }
            } else {
                // Fallback when no audio element (simulation)
                console.log('Playing patient audio introduction');
                
                // Toggle play/pause button
                this.classList.toggle('playing');
                
                // Simulate audio playing with changing waveform
                const waveform = document.querySelector('.waveform-placeholder');
                if (waveform) {
                    waveform.style.backgroundSize = '5% 100%';
                    
                    // Reset waveform after "audio" finishes
                    setTimeout(() => {
                        waveform.style.backgroundSize = '15% 100%';
                        playButton.classList.remove('playing');
                    }, 3000);
                }
            }
        });
    }
    
    // Voice input simulation
    const voiceInputBtn = document.getElementById('voice-input');
    if (voiceInputBtn) {
        voiceInputBtn.addEventListener('click', function() {
            // Simulate voice recording
            this.classList.add('recording');
            
            // In a real implementation, this would start recording
            console.log('Recording voice input...');
            
            // Add placeholder text to show it's "listening"
            const textArea = document.getElementById('user-message');
            if (textArea) {
                const originalPlaceholder = textArea.placeholder;
                textArea.placeholder = 'Listening...';
                
                // Simulate voice recognition result
                setTimeout(() => {
                    textArea.value = 'Can you tell me more about your pain? When did it start?';
                    textArea.placeholder = originalPlaceholder;
                    voiceInputBtn.classList.remove('recording');
                }, 2000);
            }
        });
    }
    
    // Same for diagnosis voice input
    const diagnosisVoiceBtn = document.getElementById('diagnosis-voice-input');
    if (diagnosisVoiceBtn) {
        diagnosisVoiceBtn.addEventListener('click', function() {
            this.classList.add('recording');
            
            const textArea = document.getElementById('diagnosis-message');
            if (textArea) {
                const originalPlaceholder = textArea.placeholder;
                textArea.placeholder = 'Listening...';
                
                setTimeout(() => {
                    textArea.value = 'Based on the right lower quadrant pain and mild anorexia, I\'m considering appendicitis as a leading diagnosis.';
                    textArea.placeholder = originalPlaceholder;
                    diagnosisVoiceBtn.classList.remove('recording');
                }, 2000);
            }
        });
    }
    
    // Order imaging button
    const orderImagingBtn = document.getElementById('order-imaging');
    if (orderImagingBtn) {
        orderImagingBtn.addEventListener('click', function() {
            // Add an AI message suggesting imaging
            const chatMessages = document.getElementById('chat-messages');
            if (chatMessages) {
                const aiMessage = document.createElement('div');
                aiMessage.className = 'message patient';
                aiMessage.innerHTML = '<p>The pain has been getting worse over the last 24 hours. It started around my belly button but now it\'s more on the lower right side.</p>';
                chatMessages.appendChild(aiMessage);
                
                // Simulation doctor's suggestion
                const doctorMessage = document.createElement('div');
                doctorMessage.className = 'message system';
                doctorMessage.innerHTML = '<p>Based on the symptoms, it would be appropriate to order imaging to confirm your suspicion.</p>';
                chatMessages.appendChild(doctorMessage);
                
                // Enable proceed button
                const proceedBtn = document.getElementById('proceed-diagnosis');
                if (proceedBtn) {
                    proceedBtn.disabled = false;
                }
                
                // Scroll to bottom
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        });
    }

    // Initialize X-ray image viewing
    initializeImageViewing();
    
    // Initialize expandable sections
    initializeExpandableSections();
}

/**
 * Initialize Case Filters on Cases Page
 */
function initializeCaseFilters() {
    const filters = document.querySelectorAll('.filter-group select, .filter-group input');
    
    filters.forEach(filter => {
        filter.addEventListener('change', function() {
            // In a real implementation, this would filter the cases
            console.log('Filtering cases by:', this.name, this.value);
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            console.log('Searching for:', this.value);
            
            // Simple client-side filtering for demonstration
            const searchTerm = this.value.toLowerCase();
            const caseCards = document.querySelectorAll('.case-card');
            
            caseCards.forEach(card => {
                const caseName = card.querySelector('h3').textContent.toLowerCase();
                const complaint = card.querySelector('.complaint-badge').textContent.toLowerCase();
                
                if (caseName.includes(searchTerm) || complaint.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Initialize image viewing functionality for X-rays
 */
function initializeImageViewing() {
    // Create modal for fullscreen viewing
    const modal = document.createElement('div');
    modal.className = 'imaging-modal';
    modal.innerHTML = `
        <div class="imaging-modal-close">&times;</div>
        <div class="imaging-modal-content">
            <img src="" alt="Enlarged X-ray image">
        </div>
    `;
    document.body.appendChild(modal);
    
    // Set up click handlers for all X-ray images
    const xrayImages = document.querySelectorAll('.imaging-image');
    xrayImages.forEach(img => {
        img.addEventListener('click', function() {
            const modalImg = modal.querySelector('img');
            modalImg.src = this.src;
            modal.classList.add('active');
        });
    });
    
    // Close modal when clicking the X or outside the image
    const closeBtn = modal.querySelector('.imaging-modal-close');
    closeBtn.addEventListener('click', function() {
        modal.classList.remove('active');
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });
    
    // Allow keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
    });
}

// Add expandable sections for detailed patient info
function initializeExpandableSections() {
    const toggleButtons = document.querySelectorAll('.details-toggle');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = this.nextElementSibling;
            this.classList.toggle('expanded');
            content.classList.toggle('expanded');
        });
    });
} 