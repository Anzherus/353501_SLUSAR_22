/* ========================================
   ЛОАДЕР ПРИ ПЕРЕХОДЕ МЕЖДУ СТРАНИЦАМИ
   Показывает прелоадер на 2-3 секунды при навигации
   ======================================== */

(function() {
    'use strict';
    
    // Минимальное время показа лоадера (2.5 секунды)
    const MIN_LOADER_TIME = 2500;
    
    // Функция для показа лоадера
    function showPageLoader() {
        // Проверяем, есть ли уже лоадер
        let loader = document.getElementById('pageTransitionLoader');
        
        if (!loader) {
            // Создаем HTML структуру лоадера
            const loaderHTML = `
                <div class="loader-container" id="pageTransitionLoader">
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
                        
                        <!-- Прогресс бар -->
                        <div class="loader-progress">
                            <div class="loader-progress-bar"></div>
                        </div>
                        
                        <p class="loader-text">Загружаем страницу...</p>
                    </div>
                </div>
            `;
            
            // Добавляем в начало body
            document.body.insertAdjacentHTML('afterbegin', loaderHTML);
            loader = document.getElementById('pageTransitionLoader');
        }
        
        // Показываем лоадер
        loader.style.display = 'flex';
        loader.classList.remove('hidden', 'fade-out');
        loader.classList.add('fade-in');
        
        return loader;
    }
    
    // Функция для скрытия лоадера
    function hidePageLoader(loader) {
        if (!loader) {
            loader = document.getElementById('pageTransitionLoader');
        }
        
        if (loader) {
            loader.classList.add('fade-out');
            
            setTimeout(() => {
                loader.style.display = 'none';
                loader.classList.remove('fade-out', 'fade-in');
            }, 600);
        }
    }
    
    // Обработчик клика по внутренним ссылкам
    function handleLinkClick(event) {
        const link = event.target.closest('a');
        
        // Проверяем, что это внутренняя ссылка
        if (link && link.href && !link.target && !link.hasAttribute('download')) {
            const url = new URL(link.href);
            const currentUrl = new URL(window.location.href);
            
            // Проверяем, что это ссылка на тот же домен
            if (url.origin === currentUrl.origin && url.pathname !== currentUrl.pathname) {
                // Игнорируем якорные ссылки
                if (!url.hash || url.pathname !== currentUrl.pathname) {
                    // Показываем лоадер
                    const loader = showPageLoader();
                    const startTime = Date.now();
                    
                    // Предотвращаем стандартное поведение
                    event.preventDefault();
                    
                    // Переходим на новую страницу с задержкой
                    setTimeout(() => {
                        window.location.href = link.href;
                    }, MIN_LOADER_TIME);
                }
            }
        }
    }
    
    // Добавляем обработчик событий при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        // Слушаем клики по всем ссылкам
        document.addEventListener('click', handleLinkClick);
        
        // Скрываем лоадер при загрузке страницы (если он есть)
        const loader = document.getElementById('pageTransitionLoader');
        if (loader) {
            setTimeout(() => {
                hidePageLoader(loader);
            }, 100);
        }
    });
    
    // Скрываем лоадер при возврате назад/вперед
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            const loader = document.getElementById('pageTransitionLoader');
            if (loader) {
                hidePageLoader(loader);
            }
        }
    });
    
})();
