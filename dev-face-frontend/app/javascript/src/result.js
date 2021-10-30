if(location.pathname == "/result") {
  $(function() {
	 let allCards = document.querySelectorAll('.swipe--card');
    function initCards() {
      let newCards = document.querySelectorAll('.swipe--card:not(.removed)');
      let img = newCards[0].getElementsByTagName("img")

      get_result_img(img)
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

    function get_result_img(img){
      $.ajax({
        url: "https://jphack-teamworker.tk/api/get_image",
        type: "GET",
        datatype: "json",
	//contentType: 'application/JSON',
        data: {
          "user_id": "masaru"
        },
        success: function(data) {
	  console.log("done");
	  img[0].setAttribute("src", data["image"]);
	},
	error: function(err) {
	  console.log("err")
	  console.log(err)
	}
      });
      /*.done(function (result) {
	      console.log(done)
	      console.log(result["image"])
	img[0].setAttribute("src", result["image"])
      })*/
    }
  });
};
