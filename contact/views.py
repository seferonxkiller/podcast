from django.shortcuts import render, redirect
from .forms import ContactForm, SubForm


def contact(request):
    form = ContactForm(request.POST or None)
    forms = SubForm(request.POST or None)
    if forms.is_valid():
        forms.save()
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ContactForm(data=request.POST)
            print('request.post iwladi')
            if form.is_valid():
                print('valid')
                obj = form.save(commit=False)
                obj.name = request.user.profile.get_full_name
                obj.save()
                return redirect(".")
        else:
            form = ContactForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(".")
    ctx = {
        'form': form,
        'forms': forms
    }
    return render(request, 'contact.html', ctx)
