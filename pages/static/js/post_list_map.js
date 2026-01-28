let map = null;

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

    cards.forEach(card => {
        let lat = card.getAttribute('data-lat');
        let lng = card.getAttribute('data-lng');
        const address = card.getAttribute('data-post-address');
        const name = card.getAttribute('data-post-name');
        const url = card.getAttribute('data-post-url');

        if (lat && lng) {
            lat = parseFloat(lat.replace(',', '.'));
            lng = parseFloat(lng.replace(',', '.'));

            const placemark = new ymaps.Placemark([lat, lng], {
                balloonContent: `<a href="${url}">${name}</a><br>${address}`
            });

            map.geoObjects.add(placemark);
        }
    });
}

function setupButtons() {
    document.querySelectorAll('.show-on-map').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const card = document.querySelector(`[data-post-id="${postId}"]`);
            if (card) {
                let lat = parseFloat(card.getAttribute('data-lat').replace(',', '.'));
                let lng = parseFloat(card.getAttribute('data-lng').replace(',', '.'));

                map.setCenter([lat, lng], 15);
            }
        });
    });
}