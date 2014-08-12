$(document).ready(function(){
  var name, cost, credit;
  $('.edit').click(function(){
    var self = this;
    var $name = $('.cardName',$(self).parent().parent());
    var $cost = $('.cardCost',$(self).parent().parent());
    var $credit = $('.cardCredit',$(self).parent().parent());
    name = $name.html();
    cost = $cost.html();
    credit = $credit.html();
    $name.html('<input class="form-control" value="'+$name.html()+'" />');
    $cost.html('<input class="form-control" value="'+$cost.html()+'" />');
    $credit.html('<input class="form-control" value="'+$credit.html()+'" />');
    $(self).hide();
    $('.save', $(self).parent()).show();
  });
  $('.save').click(function(){
    var self = this;
    var $name = $('.cardName',$(self).parent().parent());
    var $cost = $('.cardCost',$(self).parent().parent());
    var $credit = $('.cardCredit',$(self).parent().parent());
    var newName = $name.children().first().val();
    var newCost = $cost.children().first().val();
    var newCredit = $credit.children().first().val();
    var id = $('.cardId',$(self).parent().parent()).html();
    if (name == newName && cost == newCost && credit == newCredit) {
      $name.html(newName);
      $cost.html(newCost);
      $credit.html(newCredit);
      $('.save', $(self).parent()).hide();
      $('.edit', $(self).parent()).show();
    } else {
      $.ajax({
        url: '/card/',
        type: 'PUT',
        data: {
          id: id,
          cardName: newName,
          cardCost: newCost,
          cardCredit: newCredit
        }
      }).done(function(data){
        $name.html(newName);
        $cost.html(newCost);
        $credit.html(newCredit);
        $('.save', $(self).parent()).hide();
        $(self).show();
      }).fail(function(data){
        console.log('something went wrong');
      });
    }
  });
  $('.delete').click(function(){
    var self = this;
    var r = confirm('Are you sure you want to delete this?');
    if(r===true) {
      var id = $('.cardId',$(self).parent().parent())[0].innerHTML;
      $.ajax({
        url: '/card/',
        type: 'DELETE',
        data: {
          id: id
        }
      }).done(function(data){
        $(self).parent().parent().remove();
      }).fail(function(data){
        console.log('something went wrong');
      });
    }
  });
});
