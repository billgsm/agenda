jQuery(function($) {
  /******************** Useful var ********************/
  var current_url = $(location).attr('href');
  /****************************************************/
  // Customized accordion
  $('#id_date').datepicker();
  $('#content > ul > li > :not(h3)').hide();
  $('.title').click(function(e) {
    $(this).parent().parent().children(':not(h3)').slideToggle();
    e.preventDefault();
  });
  //Ajax: add participants to an event
  $(document).on("submit", '#participant_form', function(e) {
    if (current_url.indexOf("update") < 0 && current_url.indexOf("create") < 0){
    $.ajax(
      {
        type: "POST",
        data: $(this).serialize(),
        url: "",
        success: function(data) {
          if(typeof(data) == 'string'){
            element = $('#participant_form');
            element.after(data);
            element.remove();
          } else {
            element = $('#participant_form');
            element.after(data.form);
            element.remove();
            $('#participants').append(
              "<div>"
             + data.participant + " | "
             + data.get_status_display + ""
             + data.delete_form +
              "</div>"
              );
          }
        },
      }
      );
    e.preventDefault();
    }
  });

  //Ajax: remove participants from an event
  $(document).on('submit', '.delete', function(e) {
    if( $(this).attr('action').indexOf('/participant/') >= 0 ) {
      var form = $(this);
      $.ajax(
      {
        type: "POST",
        data: $(this).serialize(),
        url: $(this).attr('action'),
        success: function(data) {
          if(data.ack == 'OK') {
            form.parent(':not(#content)').remove();
            element = $('#participant_form');
            element.after(data.form);
            element.remove();
          }
        }
      });
      e.preventDefault();
    }
  });
});
