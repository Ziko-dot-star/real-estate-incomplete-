var navLinks = document.getElementById("navLinks");

function showMenu() {
    navLinks.style.right = "0";
}

function hideMenu() {
    navLinks.style.right = "-200px";
}

// Close menu when clicking outside on mobile
document.addEventListener('click', function(event) {
    var isClickInside = navLinks.contains(event.target);
    var menuBtn = document.querySelector('.fa-bars');
    
    if (!isClickInside && event.target !== menuBtn && navLinks.style.right === "0px") {
        hideMenu();
    }
});
