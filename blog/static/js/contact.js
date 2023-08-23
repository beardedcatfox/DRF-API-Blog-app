(function(w,d,$){
  $(d).ready(function(){

    let loadForm = function() {
      let btn = $(this);
      $.ajax({
        url: btn.attr("href"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#contactModal").modal("show");
        },
        success: function (data) {
          $("#contactModal .modal-content").html(data.html_form);
        }
      });
      return false;
    };

    let saveForm = function() {
        let form = $('#contact-form');
        let btn = $("#submit-btn"); // select the button using its id
        $.ajax({
            url: '/blog/contact_us/',
            data: form.serialize(),
            type: 'post',
            dataType: 'json',
            beforeSend: function() {
                btn.prop('disabled', true); // disable the button before the request is sent
            },
            success: function(data) {
              if (data.form_is_valid) {
                // display success message in modal window
                $("#contactModal .modal-content").html("<p>Thank you for your message!</p>");
                // hide modal window after 2 seconds
                setTimeout(function() {
                  $("#contactModal").modal("hide");
                }, 2000);
              } else {
                // replace the form with any validation errors
                $("#contactModal .modal-content").html(data.html_form);
              }
            },
        });
        return false;
    };

    // let saveForm = function() {
    //     let form = $('#contact-form');
    //     let btn = $("#submit-btn"); // select the button using its id
    //     $.ajax({
    //       url: '/blog/contact_us/',
    //       data: form.serialize(),
    //       type: 'post',
    //       dataType: 'json',
    //       beforeSend: function() {
    //         btn.prop('disabled', true); // disable the button before the request is sent
    //       },
    //       success: function(data) {
    //         if (data.form_is_valid) {
    //           // close the modal window
    //           $('#contactModal').modal('hide');
    //           // display a success message
    //           alert('Thank you for your message!');
    //           // optionally redirect the user
    //           // window.location.href = '/thank-you/';
    //         } else {
    //           // replace the form with any validation errors
    //           $("#contactModal .modal-content").html(data.html_form);
    //         }
    //       },
    //       error: function(xhr, textStatus, errorThrown) {
    //         // handle any errors
    //         $("#errorModal").modal("show");
    //       },
    //       complete: function() {
    //         btn.prop('disabled', false); // enable the button after the request is complete
    //       }
    //     });
    //     return false;
    //   };
    // let saveForm = function() {
    //   let form = $('#contact-form');
    //   let btn = $("#submit-btn"); // select the button using its id
    //   $.ajax({
    //     url: '/blog/contact_us/',
    //     data: form.serialize(),
    //     type: 'post',
    //     dataType: 'json',
    //     beforeSend: function() {
    //       btn.prop('disabled', true); // disable the button before the request is sent
    //     },
    //     success: function(data) {
    //         $("#contactModal .modal-content").html(data.html_form);
    //       },
    //       error: function(xhr, textStatus, errorThrown) {
    //         $("#errorModal").modal("show");
    //       },
    //       complete: function() {
    //         btn.prop('disabled', false); // enable the button after the request is complete
    //       }
    //     });
    //     return false;
    //   };


    $("body").on('click', '.js-load-form', loadForm);
    $("body").on('click', "#submit-btn", saveForm);
  })
})(window,document,jQuery);
