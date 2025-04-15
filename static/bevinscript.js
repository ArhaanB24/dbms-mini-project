$(document).ready(function(){
    $(".second").hide();
    $(".already-member").click(function(){
      $(".first").css({
          'transform': 'rotateY(180deg)'
      });
      setTimeout(function() {
          $(".first").hide();
          $(".second").css({
              'transform': 'rotateY(0deg)',
              'display': 'flex',
              'box-shadow': '0 0 20px 0 rgba(0, 0, 0, 0.2)'
          });
      },190); // Match the transition duration
    });

    $(".first-time").click(function(){
      $(".second").css({
          'transform': 'rotateY(180deg)'
      });
      setTimeout(function() {
          $(".second").hide();
          $(".first").css({
              'transform': 'rotateY(0deg)',
              'display': 'flex',
              'box-shadow': '0 0 20px 0 rgba(0, 0, 0, 0.2)'
          });
      }, 190); // Match the transition duration
    });
});



