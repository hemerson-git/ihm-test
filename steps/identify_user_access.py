from behave import given, when, then
from smart_tv import *


@given("that the recognize environment was successfully set up")
def given_setuped_recognize_environment(context):
    context.stream_services, context.configs, context.recognized_users, context.faker_generator = prepare()
    context.recognized_users = {}

    assert context.stream_services is not None


@when("the picture {person_picture} is taken by the camera")
def when_user_picture_capture(context, person_picture):
    detected_person = simulate_detect_user(person_picture)

    context.is_recognized, context.user = recognize_user(
        detected_person, context.configs, context.faker_generator, context.stream_services)

    assert True


@then("A Registered User must be recognized")
def then_recognize_registered_user(context):
    access_id = secrets.token_hex(nbytes=16).upper()
    context.recognized_users[access_id] = context.user

    assert context.is_recognized is True


@then("A Unregistered User must not to be recognized")
def then_dont_recognize_unregistered_user(context):
    assert context.is_recognized is False
