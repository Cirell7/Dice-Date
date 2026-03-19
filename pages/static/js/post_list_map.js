let map = null;
let placemarks = {}; // Объект для хранения меток по ID постов

ymaps.ready(function() {
    map = new ymaps.Map('posts-map', {
        center: [55.76, 37.64],
        zoom: 10
    });

    addPostsToMap();
    setupButtons();
});

function addPostsToMap() {
    const cards = document.querySelectorAll('.post-card');
    let bounds = []; // Для автоматического центрирования карты по всем меткам

    cards.forEach(card => {
        const postId = card.getAttribute('data-post-id');
        let lat = card.getAttribute('data-lat');
        let lng = card.getAttribute('data-lng');
        const address = card.getAttribute('data-post-address');
        const name = card.getAttribute('data-post-name');
        const url = card.getAttribute('data-post-url');

        if (lat && lng) {
            // Заменяем запятую на точку и преобразуем в число
            lat = parseFloat(lat.replace(',', '.'));
            lng = parseFloat(lng.replace(',', '.'));

            if (!isNaN(lat) && !isNaN(lng)) {
                // Создаем метку
                const placemark = new ymaps.Placemark([lat, lng], {
                    balloonContent: `<b>${name}</b><br>${address}<br><a href="${url}">Подробнее</a>`,
                    hintContent: name
                }, {
                    preset: 'islands#redDotIcon'
                });

                // Добавляем метку на карту
                map.geoObjects.add(placemark);
                
                // Сохраняем метку в объект по ID поста
                placemarks[postId] = placemark;
                
                // Добавляем координаты для расчета границ
                bounds.push([lat, lng]);
            }
        }
    });

    // Если есть метки, центрируем карту по ним
    if (bounds.length > 0) {
        map.setBounds(bounds, {
            checkZoomRange: true,
            zoomMargin: 50
        });
    }
}

function setupButtons() {
    document.querySelectorAll('.show-on-map').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const postId = this.getAttribute('data-post-id');
            console.log('Клик по кнопке для поста:', postId); // Отладка
            
            // Получаем метку по ID поста
            const placemark = placemarks[postId];
            
            if (placemark) {
                // Получаем координаты метки
                const coords = placemark.geometry.getCoordinates();
                
                // Центрируем карту на метке
                map.setCenter(coords, 15, {
                    duration: 300 // Анимация перехода
                });
                
                // Открываем баллун метки
                placemark.balloon.open();
                
                // Подсвечиваем пост (опционально)
                highlightPost(postId);
            } else {
                console.log('Метка не найдена для поста:', postId);
                alert('У этого мероприятия нет координат на карте');
            }
        });
    });
}

// Опциональная функция для подсветки выбранного поста
function highlightPost(postId) {
    // Убираем подсветку со всех постов
    document.querySelectorAll('.post-card').forEach(card => {
        card.classList.remove('highlighted');
    });
    
    // Добавляем подсветку выбранному посту
    const selectedCard = document.querySelector(`[data-post-id="${postId}"]`);
    if (selectedCard) {
        selectedCard.classList.add('highlighted');
        
        // Плавная прокрутка к посту
        selectedCard.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }
}