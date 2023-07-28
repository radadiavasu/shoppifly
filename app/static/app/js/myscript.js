$("#slider1, #slider2, #slider3").owlCarousel({
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
    },
  },
});

$(".plus-cart").click(function () {
  let id = $(this).attr("pid").toString();
  let quantity = this.parentNode.children[2];
  $.ajax({
    type: "GET",
    url: "/plus_cart",
    data: {
      product_id: id,
    },

    success: function (data) {
      quantity.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total_amount").innerText =
        data.total_amount + ".0";
    },
  });
});

$(".minus-cart").click(function () {
  let id = $(this).attr("pid").toString();
  let quantity = this.parentNode.children[2];

  $.ajax({
    type: "GET",
    url: "/minus_cart",
    data: {
      product_id: id,
    },

    success: function (data) {
      quantity.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total_amount").innerText =
        data.total_amount + ".0";
    },
  });
});

$(".remove-cart").click(function () {
  let id = $(this).attr("pid").toString();
  let elm = this;
  $.ajax({
    type: "GET",
    url: "/remove_cart",
    data: {
      product_id: id,
    },

    success: function (data) {
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total_amount").innerText =
        data.total_amount + ".0";
      elm.parentNode.parentNode.parentNode.remove();
    },
  });
});
