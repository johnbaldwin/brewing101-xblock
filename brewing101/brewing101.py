"""Brewing101 XBlock

This is a demonstration implementation of an edX XBlock that explores several
features:

* Different types of scopes
* Retrieving and displaying data from the containing course
* AJAX interaction between web client and server
* Studio modifiable settings
* Publishing grade for the lesson
* and more

There are two parts of this XBlock:

1. Poll - The student is asked if he/she has brewed before. This poll is
    optional the poll results are stored.

2. Exercise - The user is presented with an exercise to solve. The user is to
    calculate and enter the answer, then click the submit button.

This project was scaffolded using the xblock-sdk generator:

    workbench-make-xblock

The studio functionality is adapted from scormxblock:

    https://github.com/appsembler/edx_xblock_scorm

"""

from __future__ import print_function

import json
import math
import pkg_resources

from webob import Response

try:
    from courseware.courses import get_course_by_id
    COURSE_API_SUPPORTED = True
except ImportError:
    COURSE_API_SUPPORTED = False

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Boolean, Float, Dict
from xblock.fragment import Fragment


def resource_string(path):
    """Handy helper for getting resources from our kit."""
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")


class Brewing101XBlock(XBlock):
    """This class provides the core XBlock functionality for a poll and an
    exercise to calculate the answer to a formula.

    """

    has_score = True

    brewed_count = Integer(
        help='How many respondants say they have brewed before',
        default=0,
        scope=Scope.user_state_summary,
        )

    not_brewed_count = Integer(
        help='How many respondants say they have not brewed before',
        default=0,
        scope=Scope.user_state_summary,
        )

    answered_brewed_poll = Boolean(
        help='has this respondant replied to the poll',
        default=False,
        scope=Scope.user_state,
        )

    user_has_brewed = Boolean(
        help='how this respondant replied to the poll',
        default=False, scope=Scope.user_info)

    # Problem/exercise calcuation fields

    ratio = Float(default=1.0, scope=Scope.settings, help='')
    initial_mash_temp = Integer(default=72, scope=Scope.settings, help='')
    target_mash_temp = Integer(default=155, scope=Scope.settings, help='')

    expected_answer = Integer(default=172, scope=Scope.settings, help='')
    user_answer = Integer(default=-1, scope=Scope.user_state, help='')

    problem_score = Float(default=0, scope=Scope.user_state)
    weight = Float(default=1, scope=Scope.settings)

    def get_course_info(self):
        """Retrieves a small set of data from the containing course:

        Returns:
            a dict with
            * 'display_name' - The course display name
            * 'org' - The organization which the course belongs

        """
        def data_when_unavailable():
            return {
                'display_name': 'course display name',
                'org': 'course organization',
            }

        if COURSE_API_SUPPORTED:
            course_id = self.xmodule_runtime.course_id
            course_info = get_course_by_id(course_id)

            if course_info:
                return {
                    'display_name': course_info.display_name,
                    'org': course_info.org,
                }
            else:
                return data_when_unavailable()

        else:
            print('course api not supported (Must be in xblock-sdk workbench)')
            return data_when_unavailable()

    def student_view(self, context=None):
        """The primary view of the Brewing101XBlock, shown to students
        when viewing courses.
        """
        course_info = self.get_course_info()

        # Probably better to send these via context than instance members
        self.course_name = course_info['display_name']
        self.org_name = course_info['org']

        html = resource_string("static/html/brewing101.html")
        frag = Fragment(html.format(self=self))

        frag.add_css(resource_string("static/css/brewing101.css"))
        frag.add_javascript(resource_string("static/js/src/brewing101.js"))

        frag.initialize_js('Brewing101XBlock')
        return frag

    def studio_view(self, context=None):
        """The view provided in Studio for editing settings
        """
        html = resource_string("static/html/studio.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(resource_string("static/css/brewing101.css"))
        frag.add_javascript(resource_string("static/js/src/studio.js"))
        frag.initialize_js('Brewing101XBlock')
        return frag

    @XBlock.handler
    def studio_submit(self, request, suffix=''):
        """Handler that receives POST data in the Studio view for Studio
        configurable settings

        NOTE:
        This can be improved/DRY'd up, such as by writing a convenience
        method that iterates through the params and assigns to the instance
        vars. But, would need to make sure we handle type casting properly
        """
        self.initial_mash_temp = int(request.params['initial_mash_temp'])
        self.target_mash_temp = int(request.params['target_mash_temp'])
        self.expected_answer = int(request.params['expected_answer'])

        return Response(json.dumps({'result': 'success'}),
                        content_type='application/json')

    @XBlock.json_handler
    def submit_brewpoll(self, data, suffi=''):
        print('brewpoll called. data={}'.format(data))
        answer = data.get('poll_answer')
        if answer:
            self.answered_brewed_poll = True
            self.user_has_brewed = True if answer == 'yes' else False
            if self.user_has_brewed:
                self.brewed_count += 1
            else:
                self.not_brewed_count += 1

        return {
            'brewed_count': self.brewed_count,
            'not_brewed_count': self.not_brewed_count,
        }

    @XBlock.json_handler
    def submit_answer(self, data, suffix=''):
        """Handler that receives POST data in the LMS (student) view that
        contains the answer the student submitted for the problem

        """
        print('submit_answer called. data={}'.format(data))
        if not data:
            return {'error': 'empty answer submitted'}
        try:
            self.user_answer = int(math.ceil(float(data)))
        except ValueError:
            msg = 'Invalid answer. "{}" is not a number'.format(data)
            return {'error': msg}

        has_correct_answer = self.user_answer == self.expected_answer
        if has_correct_answer:
            self.problem_score = 1
        else:
            self.problem_score = 0
        self.publish_grade()

        return {'answerCorrect': has_correct_answer, }

    def publish_grade(self):
        """Publishes the grade to the LMS

        """
        self.runtime.publish(self, 'grade', {
            'value': self.problem_score,
            'max_value': self.weight,
            })


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench.

        """
        return [
            ("Brewing101XBlock",
             """<brewing101/>
             """),
            ("Multiple Brewing101XBlock",
             """<vertical_demo>
                <brewing101/>
                <brewing101/>
                </vertical_demo>
             """)
        ]
