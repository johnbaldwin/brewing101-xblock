/* Javascript for Brewing101XBlock. */
function Brewing101XBlock(runtime, element) {

    //$('.submit-answer-button', element).attr('disabled', true);

    /** 
    * The following three methods encapsulate underscore/lodash methods
    * We do this because 
    * A) including lodash causes a 'mismatched anonymouse define() modules' 
    *    error. See: http://requirejs.org/docs/errors.html#mismatch
    * B) xblock-sdk workbench does not provide underscore/lodash
    */
    function has_underscore() {
        return (typeof _ != 'undefined');
    }

    /**
     * Helper method to check if a value is empty or a string with just
     * whitespace.
     * Note: lodash and underscore 'isEmpty' considers a string with only 
     * whitespace to be not empty
     */
    function isEmpty(value) {
        if (has_underscore()) {
            if (_.isString(value)) {
                return _.isEmpty(value.trim());
            } else {
                return _.isEmpty(value);
            }
        } else {
            // just say it is not empty
            return false;
        }
    }

    /**
     * Returns true if the value is a boolean, false otherwise.
     */
    function isBoolean(value) {
        if (has_underscore()) {
            return _.isBoolean(value);
        } else {
            return  value === true || value === false;
        }
    }

    /**
     * Display a thank you message after user responds to poll
     */
    function showPollResults(results) {
        $('.poll-thankyou', element).text('Thank you!');
    }

    /**
     * Listen for changes in the poll radio buttons and POST the selected
     * button to the server
     */
    $('input[name=has-brewed-choice]', element).change(function() {
       var val = $('input[name=has-brewed-choice]:checked').val();
       console.log('brew poll selected '+val);
        $.ajax({
            type: "POST", 
            url: runtime.handlerUrl(element, 'submit_brewpoll'),
            data: JSON.stringify({poll_answer: val}),
            success: showPollResults
        })
    })

    /**
     * Listen to the answer input box. Disable the submit button if the box is
     * empty, otherwise enable it.
     */
    $('input[name=answer_input]', element).bind('input', function() {
        var val = $(this).val();
        //console.log('input event called ' + $(this).val());
        if (isEmpty(val)) {
            $('.submit-answer-button', element).attr('disabled', true);
        } else {
            $('.submit-answer-button', element).attr('disabled', false); 
        }
    });

    /**
     * Show message after user submits answer
     */
    function showProblemResults(result) {
        if ('error' in result) {
            console.log('got error: '+result.error);
            $('.answer-message', element).text(result.error)
        } else if ('answerCorrect' in result && isBoolean(result['answerCorrect'])) {
            var answer_msg = (result['answerCorrect']) ? 
                'Your answer is correct' : 'Your answer is incorrect';  
            $('.answer-message', element).text(answer_msg);
            $('.submit-answer-button', element).remove();
        } else {
            // TODO: Improve this with better handling
            $('.answer-message', element).text(
                'There was a problem processing your answer.');
        }
    }

    /**
     * Respond to the submit answer button click. This function makes a POST
     * call to the API server and upon success, updates the page with results
     *
     * It only supports the success case.
     *
     */
    $('.submit-answer-button', element).click(function(eventObject) {
        console.log('.submit-answer clicked');
        var answer = $('input[name=answer_input]').val();

        console.log('answer = '+ answer);

        $.ajax({
            type: "POST", 
            //url: submitAnswerHandlerUrl,
            url: runtime.handlerUrl(element, 'submit_answer'),
            data: JSON.stringify(answer),
            success: showProblemResults
        })
    });

    $(function ($) {
        // Initially disable the submit button.
        $('.submit-answer-button', element).attr('disabled', true);
    });
}
