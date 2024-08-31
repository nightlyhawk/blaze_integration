from functools import wraps
from django.http import HttpResponse, JsonResponse

def error_catch(func):
    @wraps(func)
    def wrapper_error_catch(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return wrapper_error_catch
