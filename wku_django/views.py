from django.shortcuts import render
from django.contrib.auth.decorators import login_required

""" classes for text animation in view to avoid long cycle tag """
RAINBOW_LAYERS = [
    'c-rainbow__layer--white',
    'c-rainbow__layer--orange',
    'c-rainbow__layer--red',
    'c-rainbow__layer--violet',
    'c-rainbow__layer--blue',
    'c-rainbow__layer--green',
    'c-rainbow__layer--yellow',
]


@login_required(login_url='/login')
def main_navigation_view(request):
    return render(request, 'main_navigation/main_nav.html', context={'rainbow_layers': RAINBOW_LAYERS})