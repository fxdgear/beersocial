from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from profiles.views import profile_detail

@login_required
def profile_detail_redirect(request, *args, **kwargs):
    user = request.user
    return redirect(profile_detail, user.username)

