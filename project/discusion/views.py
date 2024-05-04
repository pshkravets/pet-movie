from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect

from .models import Discus
from .forms import Comments


class DiscusionListView(ListView):
    template_name = 'discussion.html'
    queryset = Discus.objects.all()
    context_object_name = 'list'

    def post(self, request):
        form = Comments(self.request.POST)
        form.is_valid()
        print(form)
        data = form.cleaned_data
        Discus.objects.create(author=self.request.user, text=data['comment'])
        return HttpResponseRedirect(request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Comments
        return context