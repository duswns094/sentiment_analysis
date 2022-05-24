from django.http import HttpResponseForbidden

from diaryapp.models import Diary


def diary_ownership_required(func):
    def decorated(request, *args, **kwargs):
        diary = Diary.objects.get(pk=kwargs['pk'])
        if not diary.writer == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated