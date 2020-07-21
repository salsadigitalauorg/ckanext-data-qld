from behave import step
from behaving.web.steps import *  # noqa: F401, F403
from behaving.personas.steps import *  # noqa: F401, F403
from behaving.web.steps.url import when_i_visit_url
import random


@step('I go to homepage')
def go_to_home(context):
    when_i_visit_url(context, '/')


@step('I log in')
def log_in(context):

    assert context.persona
    context.execute_steps(u"""
        When I go to homepage
        And I click the link with text that contains "Log in"
        And I fill in "login" with "$name"
        And I fill in "password" with "$password"
        And I press the element with xpath "//button[contains(string(), 'Login')]"
        Then I should see an element with xpath "//a[contains(string(), 'Log out')]"
    """)


@step('I log in directly')
def log_in_directly(context):
    """
    This differs to the `log_in` function above by logging in directly to a page where the user login form is presented
    :param context:
    :return:
    """

    assert context.persona
    context.execute_steps(u"""
        When I fill in "login" with "$name"
        And I fill in "password" with "$password"
        And I press the element with xpath "//button[contains(string(), 'Login')]"
        Then I should see an element with xpath "//a[contains(string(), 'Log out')]"
    """)


@step('I fill in title with random text')
def title_random_text(context):

    assert context.persona
    context.execute_steps(u"""
        When I fill in "title" with "Test Title {0}"
    """.format(random.randrange(1000)))

@step('I log in and go to datarequest page')
def log_in_go_to_datarequest(context):

    assert context.persona
    context.execute_steps(u"""
        When I go to homepage
        And I click the link with text that contains "Log in"
        And I log in
        And I go to datarequest page
    """)

@step('I go to datarequest page')
def go_to_datarequest(context):
    when_i_visit_url(context, '/datarequest')

@step('I log in and create a datarequest')
def log_in_create_a_datarequest(context):

    assert context.persona
    context.execute_steps(u"""
        When I log in and go to datarequest page
        And I click the link with text that contains "Add Data Request"
        And I fill in title with random text
        And I fill in "description" with "Test description"
        And I press the element with xpath "//button[contains(string(), 'Create Data Request')]"
    """)
