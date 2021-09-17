/*!
* Start Bootstrap - Simple Sidebar v6.0.3 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
//
const addRecord = document.querySelector('.add__record_btn')
//const submitRecord = document.querySelector('.')
const form = document.querySelector('.form')
const priceChange24h = document.querySelectorAll('.day_change')

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
//         Uncomment Below to persist sidebar toggle between refreshes
         if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
             document.body.classList.toggle('sb-sidenav-toggled');
         }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

    if (addRecord) {
        if (localStorage.getItem('form_hidden') === 'false') {
            form.classList.remove('hidden');
        }
    }

});

window.setTimeout(function () {
    window.location.reload();
}, 30000);

addRecord.addEventListener('click', function(){
    form.classList.toggle('hidden');
    localStorage.setItem('form_hidden', form.classList.contains('hidden'));
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

