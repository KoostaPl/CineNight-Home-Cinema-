const carouselWrapper = document.querySelector('.carousel-wrapper');

// Пауза анимации при наведении
carouselWrapper.addEventListener('mouseover', () => {
    carouselWrapper.style.animationPlayState = 'paused';
});

carouselWrapper.addEventListener('mouseout', () => {
    carouselWrapper.style.animationPlayState = 'running';
});

// Прокрутка карусели
let currentIndex = 0;

function scrollCarousel() {
    const totalItems = document.querySelectorAll('.movie-item').length;
    const itemWidth = document.querySelector('.movie-item').offsetWidth;

    currentIndex++;
    if (currentIndex >= totalItems) {
        currentIndex = 0; // Возвращаемся к началу
    }

    // Прокручиваем карусель
    carouselWrapper.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
}

// Запуск автоматической прокрутки
setInterval(scrollCarousel, 3000); // Прокрутка каждые 3 секунды

// Функция прокрутки к началу страницы
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Отображение кнопки "Наверх"
window.onscroll = function () {
    const button = document.querySelector('.scroll-to-top');

    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        button.style.display = 'block';
    } else {
        button.style.display = 'none';
    }
};


