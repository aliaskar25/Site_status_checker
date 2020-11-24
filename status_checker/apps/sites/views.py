from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Site

from .forms import SiteIntervalForm


def statuses(request):
    sites = Site.objects.all()
    if request.method == 'POST':
        form = SiteIntervalForm()
        if form.is_valid():
            print(form)
    return render(request, 'sites_list.html', locals())

@login_required
def get_site(request, pk):
    site = Site.objects.get(pk=pk)
    if request.method == 'POST':
        form = SiteIntervalForm(request.POST)
        if form.is_valid():
            site.interval_check = form.cleaned_data['interval_time']
            site.save()
            return redirect('sites_statuses_url')
    else:
        current_interval_time = site.interval_check
        form = SiteIntervalForm(initial={'interval_time': current_interval_time})
    return render(request, 'site.html', locals())
