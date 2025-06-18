/* Ouverture et fermeture du menu */
    // Ouverture du menu déroulant
    document.addEventListener("DOMContentLoaded", function () {
        const menuButton = document.getElementById("dropdownMenuButton");
        //const menuButton = document.getElementsByClassName(".dropdown-toggle")
        const closeButton = document.getElementById("closeMenuButton");
        const menu = document.querySelector(".dropdown-menu");
    
        if (menuButton && closeButton && menu) {
            // Ouvrir le menu déroulant au clic
            menuButton.addEventListener("click", function (event) {
                event.preventDefault(); // Empêche le comportement par défaut du lien
                menu.classList.toggle("show"); // Basculer entre affiché/caché
            });
    
            // Fermer le menu déroulant avec l'icône de la croix
            closeButton.addEventListener("click", function () {
                menu.classList.remove("show"); // Supprime la classe "show"
            });
    
            // Fermer le menu si on clique en dehors
            document.addEventListener("click", function (event) {
                if (!menu.contains(event.target) && event.target !== menuButton) {
                    menu.classList.remove("show");
                }
            });
        }
    });

/* Zoom */
    document.addEventListener("wheel", function(event){
        if (event.ctrlKey) {
            event.preventDefault(); // Empêche le zoom par défaut du navigateur

            let zoomContainer = document.querySelector(".zoom-container");
            let currentScale = parseFloat(zoomContainer.computedStyleMap.transform.replace("scale(", "").replace(")", "")) || 1;

            if (event.deltaY < 0) {
                currentScale += 0.1; // Zoom avant
            } else if (event.deltaY > 0 && currentScale > 0.5) {
                currentScale -= 0.1; // Zoom arrière (limité à 50%)
            }

            zoomContainer.computedStyleMap.transform = 'scale(${currentScale})';
        }
    }, { passive: false });
