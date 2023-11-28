$(document).ready(function() {
    // Post fade in effect
    $(".post").hide().each(function(index) {
        $(this).delay(400*index).fadeIn(2000);
    });

    // Submit button hover effect
    $(".post-submit-button").hover(function(){
        $(this).animate({opacity: '0.8'}, 200);
    }, function(){
        $(this).animate({opacity: '1'}, 200);
    });

});