/*!
* Start Bootstrap - Simple Sidebar v6.0.3 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
//
import coinMarketView from './coinMarketView.js'
import { loadData, state } from './model.js'

const searchTrade = document.querySelector('.search_trade__btn')
const form = document.querySelector('.form')
const coinProfit = document.querySelector('.coin_profit')

// Fetch Market Data every 30 sec, if data is different
// page content will change without refresh.
window.setInterval(async function () {
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard'){
        const data = await loadData()
        if (data === 'diff') {
            console.log('✨✨✨')
            coinMarketView.renderMarkup(state.result.slice(0,30))
            coinMarketView.priceChangeColor()
        }
    }
}, 30000);

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
});

searchTrade.addEventListener('click', function(){
    form.classList.toggle('hidden');
    localStorage.setItem('form_hidden', true);
})

const init = async function() {
    await loadData()
    coinMarketView.renderMarkup(state.result.slice(0,30))
    coinMarketView.priceChangeColor()
}
init()