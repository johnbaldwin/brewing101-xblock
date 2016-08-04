"""
Tests of the Brewing101 XBlock, and its components.

This is adapted from the tests in the xblock-sdk sample xblock, basic

	https://github.com/edx/xblock-sdk

"""

import json

import webob

from xblock.test.tools import assert_equals

from workbench.runtime import WorkbenchRuntime

def make_request(body):
    """Mock request method."""
    request = webob.Request({})
    request.body = body
    request.method = "POST"
    return request

def text_of_response(response):
    """Return the text of response."""
    return "".join(response.app_iter)

def test_correct_answer_submission():
	runtime = WorkbenchRuntime()
	# WorkbenchRuntime has an id_generator, but most runtimes won't
	# (because the generator will be contextual), so we
	# pass it explicitly to parse_xml_string.
	brewing101_usage_id = runtime.parse_xml_string("""
		<brewing101/>
 	""", runtime.id_generator)

	brewing101 = runtime.get_block(brewing101_usage_id)
	json_data = json.dumps(172)
	resp = runtime.handle(brewing101, 'submit_answer', make_request(json_data))
	resp_data = json.loads(text_of_response(resp))
	print(resp_data)
	assert_equals(resp_data['answerCorrect'], True)