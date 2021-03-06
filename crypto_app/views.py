import requests
from .models import Website_users
from datetime import datetime
from binance import Client
from binance.exceptions import BinanceAPIException
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from crypto_app import config

# RQST_FROM_GECKO = requests.get(url=config.COIN_GECKO_URL).json()

class GetUserInfo:
    def __init__(self):
        self.api_key = None
        self.secret_key = None
        self.ALL_TICKERS = config.ALL_TICKERS

    def get_trades_info(self, symbol='BTCUSDT'):
        client = Client(self.api_key, self.secret_key)
        this_coin = {
            'new_trade': {},
            'profit': 0,
            'totle_costs': 0,
            'totle_amount': 0,
            'realized_profit': 0,
            'unrealized_profit': 0,
        }
        if symbol in self.ALL_TICKERS:
            recent_price = float(client.get_recent_trades(symbol=symbol)[0]['price'])
            this_coin['new_trade'] = client.get_my_trades(symbol=symbol)

            # Calc totole_costs and totle_amount
            for trade in this_coin['new_trade']:
                if trade['isBuyer']:
                    this_coin['totle_costs'] += float(trade['quoteQty'])
                    this_coin['totle_amount'] += float(trade['qty'])
                else:
                    this_coin['realized_profit'] += float(trade['quoteQty'])
                    this_coin['totle_amount'] -= float(trade['qty'])
            this_coin['unrealized_profit'] = recent_price * this_coin['totle_amount']
            this_coin['profit'] = this_coin['realized_profit'] + this_coin['unrealized_profit'] - this_coin[
                'totle_costs']

            # Convert timestamp to datatime
            for timestamp in this_coin['new_trade']:
                new_date = datetime.fromtimestamp((timestamp['time']) / 1000)
                timestamp['time'] = str(new_date).split(' ')[0]
            return this_coin
        else:
            return False

    def get_asset(self):
        client = Client(self.api_key, self.secret_key)
        user_asset = client.get_account()['balances']
        user_own_asset = []
        for item in user_asset:
            if float(item['free']) > 0:
                user_own_asset.append(item)
        return user_own_asset

    def get_user_status(self):
        client = Client(self.api_key, self.secret_key)
        try:
            client.get_account_status()
            return True
        except BinanceAPIException:
            return False


def home(request):
    return render(request, 'index.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = GetUserInfo()
                user.api_key = request.POST['api_key']
                user.secret_key = request.POST['secret_key']
                if user.get_user_status():
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    user_id = User.objects.get(username=request.POST['username']).id
                    api_info = Website_users(user_id=user_id, api_key=request.POST['api_key'], secret_key=request.POST['secret_key'])
                    api_info.save()
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'signup.html', {'error': 'Your API key or Secret key is invalid.'})
            except IntegrityError:
                return render(request, 'signup.html', {'error': 'That username has already been taken \n try another one.'})
        else:
            return render(request, 'signup.html', {'error': 'Password did not match.'})
    # Design from Bryan lin: https://github.com/bryanlin16899


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('dashboard')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def dashboard(request):
    user = GetUserInfo()
    try:
        user_key_info = Website_users.objects.get(user=request.user)
        user.api_key = user_key_info.api_key
        user.secret_key = user_key_info.secret_key
        if request.method == 'GET':
            return render(request, 'dashboard.html',
                          {
                           'this_coin': user.get_trades_info(),
                           'user_asset': user.get_asset()
                          })
        elif request.method == 'POST':
            new_symbol = request.POST.get('inputTicker')
            if new_symbol in user.ALL_TICKERS:
                return render(request, 'dashboard.html',
                              {
                               'this_coin': user.get_trades_info(symbol=new_symbol),
                               'user_asset': user.get_asset()
                              })
            else:
                return render(request, 'dashboard.html',
                              {
                               'error': 'Invalid Ticker',
                               'user_asset': user.get_asset()
                              })
        else:
            return render(request, 'dashboard.html',
                          {
                           'this_coin': user.get_trades_info(),
                           'user_asset': user.get_asset()
                          })
    except BinanceAPIException:
        return render(request, 'dashboard.html',
                      {
                        'error': 'Your API KEY or SECRET KEY did not correct.',
                      })


@login_required
def change_api_key(request):
    user_key_info = Website_users.objects.get(user=request.user)
    api_key = user_key_info.api_key
    secret_key = user_key_info.secret_key
    if request.method == 'GET':
        return render(request, 'change_user_api_key.html', {'api_key': api_key, 'secret_key': secret_key})
    else:
        user_key_info.api_key = request.POST['api_key']
        user_key_info.secret_key = request.POST['secret_key']
        user_key_info.save()
        return redirect('dashboard')
