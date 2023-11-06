// test function

window.onload = function() {
    var header = document.querySelector('h1.main-header');

    header.addEventListener('mouseover', function() {
        this.style.color = 'blue';
    });

    header.addEventListener('mouseout', function() {
        this.style.color = 'black';
    });
};