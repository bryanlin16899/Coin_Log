from django.shortcuts import render, redirect
from .models import Transaction_record


def home(request):
    records = Transaction_record.objects.all()
    if request.method == 'GET':
        return render(request, 'index.html', {'records': records})
    else:
        if request.POST['coin_type'] != 'Choose...' and request.POST['tran_fee'] and request.POST['price'] and request.POST['amount']:
            new_record = Transaction_record()
            new_record.date = request.POST['inputDateTime']
            new_record.buy_or_sell = request.POST['btnradio']
            new_record.type = request.POST['coin_type']
            new_record.fee = request.POST['tran_fee']
            new_record.price = request.POST['price']
            new_record.amount = request.POST['amount']
            new_record.save()
            print('success')
            return redirect(to='home')
        else:
            return render(request, 'index.html', {'error': 'Some data must be wrong format.'})


def delete_record(request, item_id):
    record = Transaction_record.objects.get(pk=item_id)
    record.delete()
    return redirect(to='home')