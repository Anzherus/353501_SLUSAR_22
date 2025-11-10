/* ========================================
   УПРАВЛЕНИЕ ЛОАДЕРОМ - КОСМЕТОЛОГИЧЕСКИЙ ЦЕНТР
   ======================================== */

class LoaderController {
    constructor(autoStart = false) {
        this.loaderContainer = null;
        this.isLoading = false;
        this.isVisible = false;
        this.minLoadTime = 2500; // Минимальное время загрузки 2.5 секунды
        this.startTime = Date.now();
        this.animationInterval = null;
        
        if (autoStart) {
            this.init();
        }
    }
    
    init() {
        // Создаем лоадер если его нет
        this.createLoader();
        
        // Запускаем загрузку
        this.startLoading();
    }
    
    createLoader() {
        // Удаляем существующий лоадер если есть
        const existingLoader = document.querySelector('.loader-container');
        if (existingLoader) {
            existingLoader.remove();
        }
        
        // Создаем HTML структуру лоадера
        const loaderHTML = `
            <div class="loader-container" id="mainLoader">
                <div class="loader-content">
                    <h1 class="loader-title">Косметологический Центр «Эстетика»</h1>
                    
                    <!-- Веерные линии -->
                    <div class="loader-bars">
                        <div class="loader-bar"></div>
                        <div class="loader-bar"></div>
                        <div class="loader-bar"></div>
                        <div class="loader-bar"></div>
                        <div class="loader-bar"></div>
                    </div>
                    
                    <!-- Стеклянные линии -->
                    <div class="loader-stack">
                        <div class="loader-stack-bar"></div>
                        <div class="loader-stack-bar"></div>
                        <div class="loader-stack-bar"></div>
                        <div class="loader-stack-bar"></div>
                        <div class="loader-stack-bar"></div>
                    </div>
                    
                    <!-- Прогресс бар -->
                    <div class="loader-progress">
                        <div class="loader-progress-bar"></div>
                    </div>
                    
                    <p class="loader-text">Загружаем для вас лучшие косметологические услуги...</p>
                </div>
            </div>
        `;
        
        // Добавляем в начало body
        document.body.insertAdjacentHTML('afterbegin', loaderHTML);
        this.loaderContainer = document.getElementById('mainLoader');
    }
    
    startLoading() {
        this.isLoading = true;
        this.isVisible = true;
        
        // Показываем лоадер
        this.show();
        
        // Симулируем загрузку ресурсов
        this.simulateLoading();
        
        // Слушаем события загрузки
        this.bindEvents();
        
        // Запускаем зацикленную анимацию
        this.startLoopAnimation();
    }
    
    simulateLoading() {
        const loadingSteps = [
            { text: 'Инициализация системы...', progress: 20 },
            { text: 'Загрузка каталога услуг...', progress: 40 },
            { text: 'Подготовка галереи...', progress: 60 },
            { text: 'Настройка интерфейса...', progress: 80 },
            { text: 'Финальная подготовка...', progress: 100 }
        ];
        
        let currentStep = 0;
        const stepInterval = 600; // 600ms между шагами
        
        const updateStep = () => {
            if (currentStep < loadingSteps.length) {
                const step = loadingSteps[currentStep];
                this.updateLoaderText(step.text);
                this.updateProgress(step.progress);
                currentStep++;
                setTimeout(updateStep, stepInterval);
            }
        };
        
        // Запускаем обновление шагов
        setTimeout(updateStep, 500);
    }
    
    updateLoaderText(text) {
        const textElement = this.loaderContainer.querySelector('.loader-text');
        if (textElement) {
            textElement.style.opacity = '0';
            setTimeout(() => {
                textElement.textContent = text;
                textElement.style.opacity = '1';
            }, 150);
        }
    }
    
    updateProgress(percentage) {
        const progressBar = this.loaderContainer.querySelector('.loader-progress-bar');
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
        }
    }
    
    bindEvents() {
        // Слушаем полную загрузку страницы
        window.addEventListener('load', () => {
            this.onPageLoaded();
        });
        
        // Слушаем готовность DOM
        if (document.readyState === 'complete') {
            this.onPageLoaded();
        }
    }
    
    onPageLoaded() {
        const elapsedTime = Date.now() - this.startTime;
        const remainingTime = Math.max(0, this.minLoadTime - elapsedTime);
        
        // Ждем минимум 2.5 секунды для плавного отображения
        setTimeout(() => {
            this.hideLoader();
        }, remainingTime);
    }
    
    startLoopAnimation() {
        // Зацикленная анимация текста
        this.animationInterval = setInterval(() => {
            if (this.isVisible && this.loaderContainer) {
                this.updateLoaderText('Загружаем для вас лучшие косметологические услуги...');
            }
        }, 2000);
    }
    
    stopLoopAnimation() {
        if (this.animationInterval) {
            clearInterval(this.animationInterval);
            this.animationInterval = null;
        }
    }
    
    hideLoader() {
        if (!this.isLoading) return;
        
        this.isLoading = false;
        this.isVisible = false;
        
        // Останавливаем зацикленную анимацию
        this.stopLoopAnimation();
        
        // Добавляем класс исчезновения
        this.loaderContainer.classList.add('fade-out');
        
        // Убираем лоадер через 500ms
        setTimeout(() => {
            if (this.loaderContainer && this.loaderContainer.parentNode) {
                this.loaderContainer.parentNode.removeChild(this.loaderContainer);
            }
        }, 500);
    }
    
    // Публичные методы для внешнего управления
    show() {
        if (this.loaderContainer) {
            this.loaderContainer.style.display = 'flex';
            this.loaderContainer.classList.remove('hidden', 'fade-out');
            this.loaderContainer.classList.add('fade-in');
            this.isVisible = true;
        }
    }
    
    hide() {
        this.hideLoader();
    }
    
    // Метод для принудительного скрытия (например, при ошибках)
    forceHide() {
        if (this.loaderContainer) {
            this.loaderContainer.style.display = 'none';
            this.loaderContainer.classList.add('hidden');
        }
    }
}

// Создаем глобальный экземпляр
let loaderController = null;

// Инициализируем при загрузке DOM (БЕЗ автоматического запуска)
document.addEventListener('DOMContentLoaded', function() {
    loaderController = new LoaderController(false); // Не запускаем автоматически
});

// Экспортируем для использования в других скриптах
window.LoaderController = LoaderController;
window.loaderController = loaderController;

// Функция для показа лоадера (зацикленного)
function showLoader() {
    // Удаляем существующий лоадер если есть
    const existingLoader = document.querySelector('.loader-container');
    if (existingLoader) {
        existingLoader.remove();
    }
    
    // Создаем HTML структуру лоадера
    const loaderHTML = `
        <div class="loader-container" id="mainLoader">
            <div class="loader-content">
                <h1 class="loader-title">Косметологический Центр «Эстетика»</h1>
                
                <!-- Веерные линии -->
                <div class="loader-bars">
                    <div class="loader-bar"></div>
                    <div class="loader-bar"></div>
                    <div class="loader-bar"></div>
                    <div class="loader-bar"></div>
                    <div class="loader-bar"></div>
                </div>
                
                <!-- Стеклянные линии -->
                <div class="loader-stack">
                    <div class="loader-stack-bar"></div>
                    <div class="loader-stack-bar"></div>
                    <div class="loader-stack-bar"></div>
                    <div class="loader-stack-bar"></div>
                    <div class="loader-stack-bar"></div>
                </div>
                
                <!-- Прогресс бар -->
                <div class="loader-progress">
                    <div class="loader-progress-bar"></div>
                </div>
                
                <p class="loader-text">Загружаем для вас лучшие косметологические услуги...</p>
            </div>
        </div>
    `;
    
    // Добавляем в начало body
    document.body.insertAdjacentHTML('afterbegin', loaderHTML);
    
    // Принудительно показываем лоадер
    const loader = document.getElementById('mainLoader');
    if (loader) {
        loader.style.display = 'flex';
        loader.style.opacity = '1';
        loader.style.zIndex = '10000';
        loader.style.position = 'fixed';
        loader.style.top = '0';
        loader.style.left = '0';
        loader.style.width = '100vw';
        loader.style.height = '100vh';
    }
}

// Функция для скрытия лоадера
function hideLoader() {
    const loader = document.querySelector('.loader-container');
    if (loader) {
        loader.remove();
    }
}

// Функция для перезапуска лоадера (для демонстрации)
function restartLoader() {
    showLoader();
}
