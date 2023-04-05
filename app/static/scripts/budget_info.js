load_budget();

function load_budget() {
    fetch('/api/family_budget/1').then(response =>
        response.json()).then(data =>{
            console.log(data);
            document.getElementById('id').value = data['id'];
            document.getElementById('type').value = "family";
            document.getElementById('money_amount').value = data['money_amount'];
            table = document.getElementsByClassName('list')[0];
            console.log(table);
            cells = table.tBodies[0].rows[0].cells;
            cells[0].innerText = data['members'][0];

            cells = table.tBodies[0].rows[1].cells;
            cells[0].innerText = data['members'][1];
        });
}

transfer_money_button = document.getElementById('transfer-money-button');
transfer_money_button.addEventListener('click', ()=> {
    window.location.href = "transfer_money.html";
});
