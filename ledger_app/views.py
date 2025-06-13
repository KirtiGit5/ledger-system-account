from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import ReceiptBookDeposit
from .forms import ReceiptBookDepositForm
from django.db.models import Sum
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
import calendar

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('receipt_list')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)  # Session expires on browser close
            return redirect('receipt_list')
        else:
            error = 'Invalid credentials'
    return render(request, 'login.html', {'error': error})

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def receipt_list(request):
    # Filters
    code = request.GET.get('code', '')
    name = request.GET.get('name', '')
    mobile = request.GET.get('mobile', '')
    month = request.GET.get('month', '')

    deposits = ReceiptBookDeposit.objects.filter(status=1)
    if code:
        deposits = deposits.filter(code__icontains=code)
    if name:
        deposits = deposits.filter(member_name__icontains=name)
    if mobile:
        deposits = deposits.filter(member_mobile__icontains=mobile)
    if month:
        deposits = deposits.filter(month__icontains=month)

    months = [choice[0] for choice in ReceiptBookDeposit.MONTH_CHOICES]

    return render(request, 'receipt_list.html', {
        'deposits': deposits.order_by('-date'),
        'months': months,
        'filters': {'code': code, 'name': name, 'mobile': mobile, 'month': month}
    })

@login_required(login_url='login')
def receipt_add(request):
    if request.method == 'POST':
        form = ReceiptBookDepositForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receipt_list')
    else:
        form = ReceiptBookDepositForm()
    return render(request, 'receipt_add.html', {'form': form, 'edit': False})

@login_required(login_url='login')
def receipt_edit(request, pk):
    deposit = get_object_or_404(ReceiptBookDeposit, pk=pk,status=1)
    if request.method == 'POST':
        form = ReceiptBookDepositForm(request.POST, instance=deposit)
        if form.is_valid():
            form.save()
            return redirect('receipt_list')
    else:
        form = ReceiptBookDepositForm(instance=deposit)
    return render(request, 'receipt_add.html', {'form': form, 'edit': True})

@login_required(login_url='login')
def month_report(request):
    months = [choice[0] for choice in ReceiptBookDeposit.MONTH_CHOICES]
    selected_month = request.GET.get('month', months[0])
    data = ReceiptBookDeposit.objects.filter(month=selected_month,status=1)

    total_debit = data.aggregate(Sum('debit_amount'))['debit_amount__sum'] or 0
    total_credit = data.aggregate(Sum('credit_amount'))['credit_amount__sum'] or 0
    total_pending = data.aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0
    total_closing = data.aggregate(Sum('closing_balance'))['closing_balance__sum'] or 0

    return render(request, 'month_report.html', {
        'months': months,
        'selected_month': selected_month,
        'data': data,
        'totals': {
            'debit': total_debit,
            'credit': total_credit,
            'pending': total_pending,
            'closing': total_closing,
        }
    })

@login_required(login_url='login')
def year_report(request):
    years = [choice[0] for choice in ReceiptBookDeposit.YEAR_CHOICES]
    selected_year = request.GET.get('year', years[0])
    data = ReceiptBookDeposit.objects.filter(year=selected_year,status=1)

    total_debit = data.aggregate(Sum('debit_amount'))['debit_amount__sum'] or 0
    total_credit = data.aggregate(Sum('credit_amount'))['credit_amount__sum'] or 0
    total_pending = data.aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0
    total_closing = data.aggregate(Sum('closing_balance'))['closing_balance__sum'] or 0

    return render(request, 'year_report.html', {
        'years': years,
        'selected_year': selected_year,
        'data': data,
        'totals': {
            'debit': total_debit,
            'credit': total_credit,
            'pending': total_pending,
            'closing': total_closing,
        }
    })

@require_POST
@login_required
def receipt_remove(request, pk):
    receipt = get_object_or_404(ReceiptBookDeposit, pk=pk)
    receipt.status = -1
    receipt.save()
    return redirect('receipt_list')