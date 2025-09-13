document.addEventListener('DOMContentLoaded', function() {
    // Progress bar functionality
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const form = document.getElementById('testeForm');
    
    if (progressBar && progressText && form) {
        // Contar o número total de perguntas pelos elementos no DOM
        const totalQuestions = document.querySelectorAll('[id^="sim_"]').length;
        let answeredQuestions = 0;
        
        // Update progress
        function updateProgress() {
            answeredQuestions = 0;
            for (let i = 0; i < totalQuestions; i++) {
                if (document.querySelector(`input[name="pergunta_${i}"]:checked`)) {
                    answeredQuestions++;
                }
            }
            
            const progress = (answeredQuestions / totalQuestions) * 100;
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);
            progressText.textContent = `${Math.round(progress)}%`;
        }
        
        // Add event listeners to all radio buttons
        const radioButtons = document.querySelectorAll('input[type="radio"]');
        radioButtons.forEach(radio => {
            radio.addEventListener('change', updateProgress);
        });
        
        // Initial progress update
        updateProgress();
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Form validation
    if (form) {
        const totalQuestions = document.querySelectorAll('[id^="sim_"]').length;
        
        form.addEventListener('submit', function(e) {
            let allAnswered = true;
            for (let i = 0; i < totalQuestions; i++) {
                if (!document.querySelector(`input[name="pergunta_${i}"]:checked`)) {
                    allAnswered = false;
                    break;
                }
            }
            
            if (!allAnswered) {
                e.preventDefault();
                
                // Criar alerta personalizado
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-warning alert-dismissible fade show';
                alertDiv.innerHTML = `
                    <strong>Atenção!</strong> Por favor, responda todas as perguntas antes de enviar o questionário.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                
                // Inserir alerta no início do formulário
                form.insertBefore(alertDiv, form.firstChild);
                
                // Scroll to first unanswered question
                for (let i = 0; i < totalQuestions; i++) {
                    if (!document.querySelector(`input[name="pergunta_${i}"]:checked`)) {
                        const questionCard = document.querySelector(`input[name="pergunta_${i}"]`).closest('.question-card');
                        if (questionCard) {
                            questionCard.scrollIntoView({
                                behavior: 'smooth',
                                block: 'center'
                            });
                            
                            // Destacar a pergunta não respondida
                            questionCard.style.boxShadow = '0 0 0 2px #ffc107';
                            setTimeout(() => {
                                questionCard.style.boxShadow = '';
                            }, 2000);
                        }
                        break;
                    }
                }
            }
        });
    }
    
    // Animation on scroll
    const animatedElements = document.querySelectorAll('.fade-in');
    
    function checkScroll() {
        animatedElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.style.opacity = 1;
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Initial check
    checkScroll();
    
    // Check on scroll
    window.addEventListener('scroll', checkScroll);
    
    // Adicionar efeitos de hover nas perguntas
    const questionCards = document.querySelectorAll('.question-card');
    questionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Botão para rolar para o topo
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '↑';
    scrollToTopBtn.className = 'btn btn-primary scroll-to-top';
    scrollToTopBtn.style.position = 'fixed';
    scrollToTopBtn.style.bottom = '20px';
    scrollToTopBtn.style.right = '20px';
    scrollToTopBtn.style.borderRadius = '50%';
    scrollToTopBtn.style.width = '50px';
    scrollToTopBtn.style.height = '50px';
    scrollToTopBtn.style.display = 'none';
    scrollToTopBtn.style.zIndex = '1000';
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    document.body.appendChild(scrollToTopBtn);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollToTopBtn.style.display = 'block';
        } else {
            scrollToTopBtn.style.display = 'none';
        }
    });
});