from django.core.cache import cache


PUBLIC_COURSE_CACHE_TIMEOUT = 300
PUBLIC_COURSE_LIST_CACHE_PATTERN = 'courses:public:list:*'


def public_course_list_cache_key(query_params):
    query_string = query_params.urlencode()
    return f"courses:public:list:{query_string or 'all'}"


def public_course_detail_cache_key(course_id):
    return f"courses:public:detail:{course_id}"


def invalidate_public_course_cache(course_id=None):
    if hasattr(cache, 'delete_pattern'):
        cache.delete_pattern(PUBLIC_COURSE_LIST_CACHE_PATTERN)

    if course_id is not None:
        cache.delete(public_course_detail_cache_key(course_id))
