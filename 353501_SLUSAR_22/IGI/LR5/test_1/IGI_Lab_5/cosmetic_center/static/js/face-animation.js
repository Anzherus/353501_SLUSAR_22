/**
 * JavaScript для управления анимацией лица и прелоадером
 */

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация прелоадера
    initPreloader();
    
    // Инициализация анимации лица
    initFaceAnimation();
});

/**
 * Инициализация прелоадера
 */
function initPreloader() {
    const preloader = document.querySelector('.preloader');
    
    if (!preloader) return;
    
    // Скрываем прелоадер через 3 секунды
    setTimeout(() => {
        preloader.classList.add('hidden');
        
        // Удаляем прелоадер из DOM через 0.5 секунды
        setTimeout(() => {
            if (preloader.parentNode) {
                preloader.parentNode.removeChild(preloader);
            }
        }, 500);
    }, 3000);
    
    // Дополнительная проверка - если страница загружена полностью, скрываем прелоадер
    window.addEventListener('load', function() {
        setTimeout(() => {
            preloader.classList.add('hidden');
            setTimeout(() => {
                if (preloader.parentNode) {
                    preloader.parentNode.removeChild(preloader);
                }
            }, 500);
        }, 1000);
    });
}

/**
 * Инициализация анимации лица
 */
function initFaceAnimation() {
    const faceContainers = document.querySelectorAll('.face-animation-container');
    
    if (!faceContainers.length) return;
    
    faceContainers.forEach((container, index) => {
        // Запускаем анимацию через небольшую задержку
        setTimeout(() => {
            startFaceAnimation(container);
        }, 500 + (index * 100));
        
        // Добавляем обработчик для повторного запуска анимации при клике
        container.addEventListener('click', function() {
            restartFaceAnimation(container);
        });
    });
}

/**
 * Запуск анимации лица
 */
function startFaceAnimation(container) {
    if (!container) {
        container = document.querySelector('.face-animation-container');
    }
    
    if (!container) return;
    
    const elements = {
        eyes: container.querySelectorAll('.eye'),
        eyebrows: container.querySelectorAll('.eyebrow'),
        nose: container.querySelector('.nose'),
        lips: container.querySelector('.lips'),
        cheeks: container.querySelectorAll('.cheek'),
        title: container.querySelector('.company-title'),
        subtitle: container.querySelector('.company-subtitle')
    };
    
    // Сбрасываем все анимации
    resetAnimations(container);
    
    // Запускаем анимации по порядку
    setTimeout(() => animateElement(elements.eyes), 1000);
    setTimeout(() => animateElement(elements.eyebrows), 1500);
    setTimeout(() => animateElement([elements.nose]), 2000);
    setTimeout(() => animateElement([elements.lips]), 2500);
    setTimeout(() => animateElement(elements.cheeks), 3000);
    setTimeout(() => animateElement([elements.title]), 4000);
    setTimeout(() => animateElement([elements.subtitle]), 4500);
}

/**
 * Перезапуск анимации лица
 */
function restartFaceAnimation(container) {
    // Сбрасываем все анимации
    resetAnimations(container);
    
    // Запускаем анимацию заново
    setTimeout(() => {
        startFaceAnimation(container);
    }, 100);
}

/**
 * Анимация элемента
 */
function animateElement(elements) {
    if (!elements) return;
    
    const elementArray = Array.isArray(elements) ? elements : [elements];
    
    elementArray.forEach(element => {
        if (element) {
            element.style.animationPlayState = 'running';
            element.style.opacity = '1';
        }
    });
}

/**
 * Сброс всех анимаций
 */
function resetAnimations(container) {
    if (!container) {
        container = document;
    }
    
    const animatedElements = container.querySelectorAll('.eye, .eyebrow, .nose, .lips, .cheek, .company-title, .company-subtitle');
    
    animatedElements.forEach(element => {
        element.style.animationPlayState = 'paused';
        element.style.animation = 'none';
        
        // Принудительно перерисовываем элемент
        element.offsetHeight;
        
        // Восстанавливаем анимацию
        element.style.animation = '';
        element.style.opacity = '0';
    });
}

/**
 * Создание эффекта частиц для прелоадера
 */
function createParticleEffect() {
    const preloader = document.querySelector('.preloader');
    if (!preloader) return;
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(preloader);
    }
}

/**
 * Создание отдельной частицы
 */
function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Случайные размеры и позиции
    const size = Math.random() * 4 + 2;
    const startX = Math.random() * window.innerWidth;
    const startY = Math.random() * window.innerHeight;
    
    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 50%;
        left: ${startX}px;
        top: ${startY}px;
        pointer-events: none;
        animation: particleFloat ${Math.random() * 3 + 2}s ease-in-out infinite;
    `;
    
    container.appendChild(particle);
    
    // Удаляем частицу через некоторое время
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 5000);
}

/**
 * Добавление CSS для анимации частиц
 */
function addParticleStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleFloat {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
                opacity: 0.8;
            }
            50% {
                transform: translateY(-20px) rotate(180deg);
                opacity: 1;
            }
        }
        
        .particle {
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        }
    `;
    document.head.appendChild(style);
}

// Инициализируем эффект частиц
document.addEventListener('DOMContentLoaded', function() {
    addParticleStyles();
    createParticleEffect();
    
    // Создаем новые частицы периодически
    setInterval(createParticleEffect, 3000);
});
