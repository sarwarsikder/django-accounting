# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from accounting.authentication_decorators import authentication_required
from .form.person_form import PersonForm, PersonFormCreate
from .models import Person


class PersonListView(ListView):
    model = Person
    template_name = 'person_list.html'  # Specify the template name
    context_object_name = 'persons'  # Specify the variable name in the template

    def get_queryset(self):
        return Person.objects.all()


@authentication_required
def persons_list(request, person_type):
    user = request.user
    if user.company and user.company_branch:
        persons = Person.objects.filter(
            company_id=user.company,
            company_branch=user.company_branch,
            person_type=person_type
        )
    else:
        # If user's company or company branch is not set, return an empty queryset
        persons = Person.objects.none()
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
        'persons': persons,
        'person_type': person_type,
    }
    return render(request, 'persons/person_list.html', {'context': context, 'persons': persons})


def person_edit(request, pk, person_type):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
        'person_type': person_type,
    }
    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            user = request.user
            person = form.save(commit=False)
            person.company_id = user.company
            person.company_branch = user.company_branch
            person.save()
            return redirect('person-list', person_type)
    else:
        form = PersonForm(instance=person)

    return render(request, 'persons/person_edit.html', {'form': form, 'context': context})


def person_delete(request, pk, person_type):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
        'person_type': person_type,
    }

    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        person.delete()
        return redirect('person-list', person_type)

    return render(request, 'persons/person_delete.html', {'person': person, 'context': context})


def person_create(request, person_type):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company': user.company,
        'company_branch': user.company_branch,
        'person_type': person_type,
    }
    if request.method == 'POST':
        form = PersonFormCreate(request.POST)
        if form.is_valid():
            user = request.user
            person = form.save(commit=False)
            person.company_id = user.company
            person.company_branch = user.company_branch
            person.save()
            return redirect('person-list', person_type)  # Redirect to the person list page after successful creation
    else:
        form = PersonFormCreate()

    return render(request, 'persons/person_create.html', {'form': form, 'context': context})
