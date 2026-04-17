from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from .models import Patient, Owner, Visit, Invoice, Universe, CareNote

def ctx(request, extra=None):
    """Helper: always include is_staff so templates can show/hide edit controls."""
    data = {'is_staff': request.user.is_staff}
    if extra:
        data.update(extra)
    return data

def home(request):
    return render(request, 'mythical_mane/home.html', ctx(request, {
        'total_patients': Patient.objects.count(),
        'total_owners': Owner.objects.count(),
        'total_visits': Visit.objects.count(),
        'total_invoices': Invoice.objects.count(),
        'recent_visits': Visit.objects.select_related('patient','vet').order_by('-visit_id')[:6],
        'recent_patients': Patient.objects.select_related('owner','universe').order_by('-patient_id')[:8],
    }))

def patients(request):
    return render(request, 'mythical_mane/patients.html', ctx(request, {
        'patients': Patient.objects.select_related('owner','universe').order_by('name'),
    }))

def visits(request):
    return render(request, 'mythical_mane/visits.html', ctx(request, {
        'visits': Visit.objects.select_related('patient','vet').order_by('-visit_id')[:100],
    }))

def owners_list(request):
    return render(request, 'mythical_mane/owners_list.html', ctx(request, {
        'owners': Owner.objects.all().order_by('name'),
    }))

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name','phone','email','address']

@staff_member_required(login_url='/admin/login/')
def owner_create(request):
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Owner created.')
        return redirect('owners_list')
    return render(request, 'mythical_mane/owner_form.html', ctx(request, {'form': form, 'action': 'Create'}))

@staff_member_required(login_url='/admin/login/')
def owner_edit(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    form = OwnerForm(request.POST or None, instance=owner)
    if form.is_valid():
        form.save()
        messages.success(request, 'Owner updated.')
        return redirect('owners_list')
    return render(request, 'mythical_mane/owner_form.html', ctx(request, {'form': form, 'action': 'Edit', 'owner': owner}))

@staff_member_required(login_url='/admin/login/')
def owner_delete(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        owner.delete()
        messages.success(request, 'Owner deleted.')
        return redirect('owners_list')
    return render(request, 'mythical_mane/owner_confirm_delete.html', ctx(request, {'owner': owner}))

def carenotes_list(request):
    return render(request, 'mythical_mane/carenotes_list.html', ctx(request, {
        'notes': CareNote.objects.select_related('patient').order_by('-created_at'),
    }))

class CareNoteForm(forms.ModelForm):
    class Meta:
        model = CareNote
        fields = ['patient','note','follow_up_date','resolved']
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type':'date'}),
            'note': forms.Textarea(attrs={'rows':4}),
        }

@staff_member_required(login_url='/admin/login/')
def carenote_create(request):
    form = CareNoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Care note created.')
        return redirect('carenotes_list')
    return render(request, 'mythical_mane/carenote_form.html', ctx(request, {'form': form, 'action': 'Create'}))

@staff_member_required(login_url='/admin/login/')
def carenote_edit(request, pk):
    note = get_object_or_404(CareNote, pk=pk)
    form = CareNoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        messages.success(request, 'Care note updated.')
        return redirect('carenotes_list')
    return render(request, 'mythical_mane/carenote_form.html', ctx(request, {'form': form, 'action': 'Edit', 'note': note}))

@staff_member_required(login_url='/admin/login/')
def carenote_delete(request, pk):
    note = get_object_or_404(CareNote, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Care note deleted.')
        return redirect('carenotes_list')
    return render(request, 'mythical_mane/carenote_confirm_delete.html', ctx(request, {'note': note}))
