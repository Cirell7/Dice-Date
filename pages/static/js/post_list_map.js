// maps.js - правильная версия
document.addEventListener('DOMContentLoaded', function() {
    // Ждем загрузки DOM перед инициализацией карты
    ymaps.ready(init);
});

let postsMap;
let placemarks = [];

function init() {
    // Проверяем что элемент карты существует
    const mapElement = document.getElementById('posts-map');
    if (!mapElement) {
        console.error('Element #posts-map not found');
        return;
    }

    // Создаем карту
    postsMap = new ymaps.Map('posts-map', {
        center: [55.76, 37.64], // Москва по умолчанию
        zoom: 10
    });

    // Добавляем метки для всех постов
    addPostsToMap();

    // Обработчик для кнопок "Показать на карте"
    document.querySelectorAll('.show-on-map').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            showPostOnMap(postId);
        });
    });
}

// Остальные функции без изменений
function addPostsToMap() {
    const postCards = document.querySelectorAll('.post-card');
    
    postCards.forEach(card => {
        const lat = card.getAttribute('data-lat');
        const lng = card.getAttribute('data-lng');
        const name = card.getAttribute('data-post-name');
        const address = card.getAttribute('data-post-address');
        const url = card.getAttribute('data-post-url');
        
        if (lat && lng) {
            const placemark = new ymaps.Placemark([parseFloat(lat), parseFloat(lng)], {
                balloonContent: `
                    <strong><a href="${url}">${name}</a></strong><br>
                    ${address}<br>
                    <a href="${url}">Перейти к встрече →</a>
                `
            }, {
                preset: 'islands#blueDotIcon'
            });
            
            postsMap.geoObjects.add(placemark);
            placemarks.push({
                id: card.getAttribute('data-post-id'),
                placemark: placemark
            });
        } else if (address) {
            ymaps.geocode(address).then(function (res) {
                const firstGeoObject = res.geoObjects.get(0);
                if (firstGeoObject) {
                    const coords = firstGeoObject.geometry.getCoordinates();
                    
                    const placemark = new ymaps.Placemark(coords, {
                        balloonContent: `
                            <strong><a href="${url}">${name}</a></strong><br>
                            ${address}<br>
                            <a href="${url}">Перейти к встрече →</a>
                        `
                    }, {
                        preset: 'islands#redDotIcon'
                    });
                    
                    postsMap.geoObjects.add(placemark);
                    placemarks.push({
                        id: card.getAttribute('data-post-id'),
                        placemark: placemark
                    });
                }
            });
        }
    });
}

function showPostOnMap(postId) {
    const postMark = placemarks.find(item => item.id === postId);
    if (postMark) {
        postMark.placemark.balloon.open();
        postsMap.setCenter(postMark.placemark.geometry.getCoordinates(), 15);
        
        document.querySelectorAll('.post-card').forEach(card => {
            card.style.backgroundColor = '';
        });
        document.querySelector(`[data-post-id="${postId}"]`).style.backgroundColor = '#f0f8ff';
    }
}