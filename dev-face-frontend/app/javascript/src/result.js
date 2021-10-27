if(location.pathname == "/result") {
  $(function() {
    function initCards() {
      let newCards = document.querySelectorAll('.swipe--card:not(.removed)');
      let img = newCards[0].getElementsByTagName("img")

      img[0].src = get_result_img()
      newCards.forEach(function (card, index) {
        card.style.zIndex = allCards.length - index;
        card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
        card.style.opacity = (10 - index) / 10;
      });

      if (newCards.length == 0) {
        $(".no-user").addClass("is-active");
      }

    }

    initCards();

    function get_result_img(){
      $.ajax({
        url: "https://jphack-teamworker.tk/api/get_image",
        type: "GET",
        datatype: "json",
        data: {
          user_id: "test",
        }
      })
      .done(function (result) {
        return result.json["image_base64"]
      })
    }
  });
};
