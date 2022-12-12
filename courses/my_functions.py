from .models import Course

def get_valid_courses(user):
    courses = list(Course.objects.all().values('id', 'users'))
    valid_courses_ids = []
    for course in courses:
        course_id = course['id']
        valid_users = course['users']
        if str(user.id) in valid_users:
            valid_courses_ids.append(course_id)
    valid_courses = Course.objects.filter(id__in=valid_courses_ids)
    return valid_courses
