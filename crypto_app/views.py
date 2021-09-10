from django.shortcuts import render, redirect
from .models import Transaction_record

def change_date_format(data):
    date_split = data.split(' ')[0].split('/')
    date_format = ''
    date_format += (date_split[2] + '-') + (date_split[0] + '-') + (date_split[1])
    return date_format

def home(request):
    records = Transaction_record.objects.all()
    if request.method == 'GET':
        return render(request, 'index.html', {'records': records})
    else:
        if request.POST['coin_type'] != 'Choose...' and request.POST['tran_fee'] and request.POST['price'] and request.POST['amount']:
            new_record = Transaction_record()
            new_record.date = change_date_format(request.POST['inputDateTime'])
            new_record.type = request.POST['coin_type']
            new_record.fee = request.POST['tran_fee']
            new_record.price = request.POST['price']
            new_record.amount = request.POST['amount']
            new_record.save()
            print('success')
            return redirect(to='home')
        else:
            return render(request, 'index.html', {'error': 'Some data must be wrong format.'})

