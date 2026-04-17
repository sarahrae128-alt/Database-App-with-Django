from django.contrib import admin
from .models import (
    Universe, Owner, Patient, Employee, Visit,
    CareNote, ProcedureDefinition, VisitDiagnosis,
    VisitProcedure, Invoice, LineItem, Payment,
    Observation, PatientAbility
)

@admin.register(Universe)
class UniverseAdmin(admin.ModelAdmin):
    search_fields = ['universe_id']

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['owner_id', 'name', 'email', 'phone']
    search_fields = ['name', 'email']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'name', 'species_id', 'color', 'dob', 'owner']
    search_fields = ['name', 'color']
    list_filter = ['species_id']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['visit_id', 'patient', 'start_at', 'reason']
    search_fields = ['reason', 'patient__name']
    date_hierarchy = 'start_at'

@admin.register(ProcedureDefinition)
class ProcedureDefinitionAdmin(admin.ModelAdmin):
    pass

@admin.register(VisitDiagnosis)
class VisitDiagnosisAdmin(admin.ModelAdmin):
    pass

@admin.register(VisitProcedure)
class VisitProcedureAdmin(admin.ModelAdmin):
    pass

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_id', 'visit', 'status', 'due_date']
    list_filter = ['status']

@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    pass

@admin.register(PatientAbility)
class PatientAbilityAdmin(admin.ModelAdmin):
    pass

@admin.register(CareNote)
class CareNoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'created_at', 'follow_up_date', 'resolved']
    list_filter = ['resolved']
    search_fields = ['note', 'patient__name']
    date_hierarchy = 'created_at'
