document.addEventListener('DOMContentLoaded', () => {  
    const navbarNav = document.getElementById('navbarNav');  
    const popupMenu = document.getElementById('popupMenu');  

    // Установка начальной видимости меню в заголовке
    navbarNav.style.display = window.innerWidth > 700 ? 'flex' : 'none';  
    popupMenu.style.display = 'none';  

    // Функция для переключения всплывающего меню
    window.toggleMenu = function() {  
        if (popupMenu.style.display === 'block') {  
            popupMenu.style.display = 'none';  
        } else {  
            popupMenu.style.display = 'block';  
        }  
    };  

    // Обработчик изменения размера окна
    window.addEventListener('resize', () => {  
        if (window.innerWidth > 700) {  
            navbarNav.style.display = 'flex';  
            popupMenu.style.display = 'none';  
        } else {  
            navbarNav.style.display = 'none';  
        }  
    });  
});