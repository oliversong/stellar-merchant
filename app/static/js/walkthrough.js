$(document).ready(function(){
  setTimeout(function(){
    $('#slide1').animate({
      'margin-top': '0px',
      'opacity': 1
      }, 400);
  }, 400);

  $('.goTo2').click(function(){
    var cardId;
    $.ajax({
      url: '/card/',
      type: 'POST',
      data: {
        cardName: $('#cardName').val(),
        cardCost: $('#cardCost').val(),
        cardCredit: $('#cardCredit').val()
      }
    }).done(function(data){
      $('#cardId').html(data);
      $('#slide1').fadeOut(200);
      $('#slide1').remove();
      $('#slide2').animate({
        'margin-top': '0px',
        'opacity': 1
        }, 400);
    }).fail(function(data){
      if (data=="not_number") {
        $('.errorBox1').html('One of your values isn\'t formatted correctly!');
      } else {
        $('.errorBox1').html('There are missing fields!');
      }
    });
  });

  $('.goTo3').click(function(){
    $('#slide2').fadeOut(200);
    $('#slide2').remove();
    $('#slide3').animate({
      'margin-top': '0px',
      'opacity': 1
      }, 400);
  });

  $('.doneDeal').click(function(){
    $.ajax({
      url: '/endpoints/',
      type: 'POST',
      data: {
        redirect_target: $('#redirect_target').val(),
        redirect_endpoint: $('#redirect_endpoint').val(),
        failure_target: $('#failure_target').val(),
        isWalkthrough: 'true'
      }
    }).done(function(data){
      debugger;
      $.ajax({
        url: '/make_active/',
        type: 'POST'
      }).done(function(data){
        window.location = '/home/';
      });
    }).fail(function(data){
      $('.errorBox2').html('There are missing fields!');
    });
  });

});
