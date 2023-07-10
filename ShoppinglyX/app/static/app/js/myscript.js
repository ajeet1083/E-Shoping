$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click( function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type : "GET",
        url : "/plus-cart",
        data : {
            prod_id:id
        },
        success : function(data){
            document.getElementById('quantity'+id).innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})

$('.minus-cart').click( function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type : "GET",
        url : "/minus-cart",
        data : {
            prod_id:id
        },
        success : function(data){
            document.getElementById('quantity'+id).innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})


$('.remove-cart').click( function(){
    var id = $(this).attr("pid").toString();
    var eml = this
    $.ajax({
        type : "GET",
        url : "/remove-cart",
        data : {
            prod_id:id
        },
        success : function(data){
         document.getElementById('amount').innerText = data.amount
         document.getElementById('total_amount').innerText = data.total_amount
         document.getElementById('shipping_amount').innerText = data.shipping_amount

         eml.parentNode.parentNode.parentNode.parentNode.remove()
           console.log(data)
        }
    })
})