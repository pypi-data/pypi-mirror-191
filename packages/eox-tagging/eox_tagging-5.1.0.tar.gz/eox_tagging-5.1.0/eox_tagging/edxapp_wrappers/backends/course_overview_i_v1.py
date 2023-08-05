"""
Backend CourseOverview file, here are all the methods from
openedx.core.djangoapps.content.course_overviews.
"""


def get_course_overview():
    """Backend to get course overview."""
    from openedx.core.djangoapps.content.course_overviews.models import \
        CourseOverview  # pylint: disable=import-outside-toplevel, import-error

    return CourseOverview
