from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from customers.models import Customer
from quotations.models import Quotation
from invoices.models import Invoice
import json

def dashboard(request):    
    customers_count = Customer.objects.all().count()
    quotation_count = Quotation.objects.all().count()
    invoice_count = Invoice.objects.all().count()
    context = {
        'customers_count': customers_count,
        'quotation_count': quotation_count,
        'invoice_count': invoice_count       
    }
    return render(request, 'dashboard/dashboard.html', context)
