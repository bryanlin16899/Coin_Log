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

window.addEventListener('DOMContentLoaded', event => {

//    // Toggle the side navigation
//    const sidebarToggle = document.body.querySelector('#sidebarToggle');
//    if (sidebarToggle) {
////         Uncomment Below to persist sidebar toggle between refreshes
//         if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
//             document.body.classList.toggle('sb-sidenav-toggled');
//         }
//        sidebarToggle.addEventListener('click', event => {
//            event.preventDefault();
//            document.body.classList.toggle('sb-sidenav-toggled');
//            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
//        });
//    }

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

window.setTimeout(function () {
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard'){
        window.location.reload();
    }
}, 30000);

searchTrade.addEventListener('click', function(){
    form.classList.toggle('hidden');
    localStorage.setItem('form_hidden', true);
})

priceChange24h.forEach( num => {
if (Number(num.textContent) > 0){
    num.style.color = 'green';
    num.textContent = `▲${num.textContent}`
} else {
    num.style.color = 'red';
    num.textContent = `▼${num.textContent}`
}
})

