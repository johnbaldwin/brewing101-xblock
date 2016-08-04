/**
 * Adapted from studio.js in: https://github.com/appsembler/edx_xblock_scorm
 */
function Brewing101XBlock(runtime, element) {

  var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

  $(element).find('.save-button').bind('click', function() {

    // This code is a candidate for refactoring to DRY it up

    var form_data = new FormData();
    var initial_mash_temp = $(element).find('input[name=initial_mash_temp]').val();
    var target_mash_temp = $(element).find('input[name=target_mash_temp]').val();
    var expected_answer = $(element).find('input[name=expected_answer]').val();

    form_data.append('initial_mash_temp', initial_mash_temp);
    form_data.append('target_mash_temp', target_mash_temp);
    form_data.append('expected_answer', expected_answer);

    runtime.notify('save', {state: 'start'});

    $.ajax({
      url: handlerUrl,
      dataType: 'text',
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      type: "POST",
      success: function(response){
        runtime.notify('save', {state: 'end'});
      }
    });

  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });

}