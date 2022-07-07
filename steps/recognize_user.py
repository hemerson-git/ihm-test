from behave import given, when, then
from smart_tv import *


@when("the User was identified")
def when_user_identified(context):
    identify_user(context.recognized_users,
                  context.user, context.is_recognized)

    assert True


@then("Verify what kind of services and resources are available to him/her")
def then_verify_services_and_resources(context):
    granted_access_user = verify_registration(
        context.recognized_users, context.stream_services)

    granted_access_user is not None
