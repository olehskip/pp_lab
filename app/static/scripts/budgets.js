load_budgets();

function load_budgets() {
    fetch('/api/user/2/budgets').then(response =>
        response.json() ).then(data =>{
            table = document.getElementById('budgets-table');
            cells = table.tBodies[0].rows[0].cells;
            cells[1].innerText = data[0]['id'];
            cells[2].innerText = data[0]['type'];
            cells[3].innerText = data[0]['money_amount'];
            cells[4].innerText = data[0]['members'];

            cells = table.tBodies[0].rows[1].cells;
            cells[1].innerText = data[1]['id'];
            cells[2].innerText = data[1]['type'];
            cells[3].innerText = data[1]['money_amount'];
            cells[4].innerText = data[1]['members'];
        });
}