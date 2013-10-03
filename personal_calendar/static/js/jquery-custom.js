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
  $('#participant_form').submit(function(e) {
    if (current_url.indexOf("update") < 0){
    $.ajax(
      {
        type: "POST",
        data: $(this).serialize(),
        url: "",
        success: function(data) {
          if(typeof(data) == 'string'){
            $("#participant_form").html(data);
          } else {
            $("#participant_form").html(data.form);
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
  $(document).on('click', '.delete', function(e) {
    e.preventDefault();
    var form = $(this);
    $.ajax(
    {
      type: "POST",
      data: $(this).serialize(),
      url: $(this).attr('action'),
      success: function(data) {
        if(data.ack == 'OK') {
          form.parent(':not(#content)').remove();
          $("#participant_form").html(data.form);
        }
      }
    });
  });
});
