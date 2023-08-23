$(document).ready(function(){
  $('.js-load-form').click(function(e){
    e.preventDefault();
    var url = $(this).attr('href');
    $('.modal-content').load(url, function(){
      $('#modal').modal({show:true});
    });
  });
});
