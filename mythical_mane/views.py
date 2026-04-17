from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django import forms
from .models import Patient, Owner, Visit, Invoice, Universe, CareNote

# ---------- DASHBOARD ----------
def home(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_owners': Owner.objects.count(),
        'total_visits': Visit.objects.count(),
        'total_invoices': Invoice.objects.count(),
        'recent_visits': Visit.objects.select_related('patient','vet').order_by('-visit_id')[:6],
        'recent_patients': Patient.objects.select_related('owner','universe').order_by('-patient_id')[:8],
    }
    return render(request, 'mythical_mane/home.html', context)

# ---------- MISSION 6: PATIENT LIST ----------
def patients(request):
    patient_list = Patient.objects.select_related('owner', 'universe').order_by('name')
    return render(request, 'mythical_mane/patients.html', {'patients': patient_list})

# ---------- VISITS ----------
def visits(request):
    visit_list = Visit.objects.select_related('patient', 'vet').order_by('-visit_id')[:100]
    return render(request, 'mythical_mane/visits.html', {'visits': visit_list})

# ---------- MISSION 8: OWNERS CRUD ----------
class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'phone', 'email', 'address']

def owners_list(request):
    owners = Owner.objects.all().order_by('name')
    return render(request, 'mythical_mane/owners_list.html', {'owners': owners})

def owner_create(request):
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Owner created successfully.')
        return redirect('owners_list')
    return render(request, 'mythical_mane/owner_form.html', {'form': form, 'action': 'Create'})

def owner_edit(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    form = OwnerForm(request.POST or None, instance=owner)
    if form.is_valid():
        form.save()
        messages.success(request, 'Owner updated successfully.')
        return redirect('owners_list')
    return render(request, 'mythical_mane/owner_form.html', {'form': form, 'action': 'Edit', 'owner': owner})

def owner_delete(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        owner.delete()
        messages.success(request, 'Owner deleted.')
        return redirect('owners_list')
    return render(request, 'mythical_mane/owner_confirm_delete.html', {'owner': owner})

# ---------- MISSION 8: CARE NOTES CRUD ----------
class CareNoteForm(forms.ModelForm):
    class Meta:
        model = CareNote
        fields = ['patient', 'note', 'follow_up_date', 'resolved']
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 4}),
        }

def carenotes_list(request):
    notes = CareNote.objects.select_related('patient').order_by('-created_at')
    return render(request, 'mythical_mane/carenotes_list.html', {'notes': notes})

def carenote_create(request):
    form = CareNoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Care note created.')
        return redirect('carenotes_list')
    return render(request, 'mythical_mane/carenote_form.html', {'form': form, 'action': 'Create'})

def carenote_edit(request, pk):
    note = get_object_or_404(CareNote, pk=pk)
    form = CareNoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        messages.success(request, 'Care note updated.')
        return redirect('carenotes_list')
    return render(request, 'mythical_mane/carenote_form.html', {'form': form, 'action': 'Edit', 'note': note})

def carenote_delete(request, pk):
    note = get_object_or_404(CareNote, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Care note deleted.')
        return redirect('carenotes_list')
    return render(request, 'mythical_mane/carenote_confirm_delete.html', {'note': note})
