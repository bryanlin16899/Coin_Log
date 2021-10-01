/*!
* Start Bootstrap - Simple Sidebar v6.0.3 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
//
const searchTrade = document.querySelector('.search_trade__btn')
//const submitRecord = document.querySelector('.')
const form = document.querySelector('.form')
const priceChange24h = document.querySelectorAll('.day_change')
const coinProfit = document.querySelector('.coin_profit')

const coin_market = document.querySelectorAll('.coin_market')
const curElement = Array.from(coin_market)

window.setTimeout(function () {
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard'){
        window.location.reload();
    }
}, 30000);

const timeout = function (s) {
  return new Promise(function (_, reject) {
    setTimeout(function () {
      reject(new Error(`Request took too long! Timeout after ${s} second`));
    }, s * 1000);
  });
};

window.addEventListener('DOMContentLoaded', event => {
    if (searchTrade) {
        if (localStorage.getItem('form_hidden') === 'false') {
            form.classList.remove('hidden');
        }
    }

    if (Number(coinProfit.textContent) > 0){
        coinProfit.style.color = 'green';
        coinProfit.textContent = `▲${coinProfit.textContent} USD`
    } else if (Number(coinProfit.textContent) < 0) {
        coinProfit.style.color = 'red';
        coinProfit.textContent = `▼${coinProfit.textContent} USD`
    } else {
        coinProfit.textContent = `0`
    }

    console.log(curElement);
});

searchTrade.addEventListener('click', function(){
    form.classList.toggle('hidden');
    localStorage.setItem('form_hidden', true);
})

const getData = async function (url) {
    try {
        const fetchData = fetch(url)
        const res = await Promise.race([fetchData, timeout(10)])

        if(!res.ok) throw new Error(`something wrong.`)
        console.log(res.json())

    } catch (err) {
        console.log(err)
    }
}

getData('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false')

priceChange24h.forEach( num => {
if (Number(num.textContent) > 0){
    num.style.color = 'green';
    num.textContent = `▲${num.textContent}`
} else {
    num.style.color = 'red';
    num.textContent = `▼${num.textContent}`
}
})

