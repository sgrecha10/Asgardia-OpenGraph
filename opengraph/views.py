"""
views.py module
"""
from django.shortcuts import render
from django.contrib import messages
from .forms import UrlForm
from .classes import OpenGraph


# Create your views here.
def opengraph_view(request):
    """This view handles the url request"""
    context = {}
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            opengraph = OpenGraph(request.POST['url'])
            if not opengraph.get_messages():
                context.update({'json_data': opengraph.get_json()})
                context.update({'list_data': opengraph.get_list()})
            else:
                for message in opengraph.get_messages():
                    messages.warning(request, message)
    else:
        form = UrlForm(initial={'url': 'https://www.youtube.com/watch?v=v_-ircfNnV8'})

    context.update({'form': form})
    return render(request, 'opengraph/index.html', context)
