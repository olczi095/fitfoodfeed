$(document).ready(function(){
    $('.like-form').submit(function(e){
        e.preventDefault();
        const review_id = $(this).find('button[name="like-btn"], button[name="unlike-btn"]').val();
        const token = $('input[name=csrfmiddlewaretoken').val();
        const url = $(this).attr('action');

        $.ajax({
            method: "POST",
            url: url,
            headers: {'X-CSRFToken': token},
            data: {
                'review_id': review_id
            },
            success: function(response){
                const likesCounterElement = $('.likes-button h5');
                likesCounterElement.text(response.likes_counter);
                console.log(response.liked);
                if (response.liked) {
                    $('.likes-button .like').addClass('unlike');
                    console.log(response.liked);

                } else {
                    $('.likes-button .like').removeClass('unlike');
                    console.log(response.liked);

                }
            },
            error: function(response){
                console.log("Failed ", response)
            },
        })
    });
})