from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.



@login_required()
def index(request):
    user_groups = request.user.groups.all()
    user_group_permissions = request.user.get_group_permissions()

    print(f'user_groups: {user_groups}')

    if request.user.groups.filter(name__in=['developers']).exists():
        return reverse('/to/developers/page')
    elif request.user.groups.filter(name__in=['devops']).exists():
        return reverse('/to/devops/page')
    elif request.user.groups.filter(name__in=['operations']).exists():
        return reverse('/to/operations/page')

    else:
        raise PermissionDenied()



    return HttpResponse('Hello home')

