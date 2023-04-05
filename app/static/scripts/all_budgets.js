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

const checkboxes = document.getElementsByClassName("chk");
var number_of_chekboxes_activated = 0;

function updated_buttons() {
    document.getElementById('view-budget-button').disabled = number_of_chekboxes_activated != 1;
    document.getElementById('delete-budget-button').disabled = number_of_chekboxes_activated == 0;
}

updated_buttons();

Array.from(checkboxes).forEach((checkbox, index) => {
    checkbox.addEventListener('click', () => {
        if (checkbox.checked) {
            if(index == 0) {
                number_of_chekboxes_activated = checkboxes.length - 1;
                Array.from(checkboxes).forEach((checkbox, index) => {
                    checkbox.checked = true;
                });
            }
            else {
                number_of_chekboxes_activated += 1;
            }

        } else {
            if(index == 0) {
                number_of_chekboxes_activated = 0;
                Array.from(checkboxes).forEach((checkbox, index) => {
                    checkbox.checked = false;
                });
            }
            else {
                number_of_chekboxes_activated -= 1;
                checkboxes[0].checked = false;
            }
        }
        updated_buttons();
    });
  });

view_button = document.getElementById('view-budget-button');
view_button.addEventListener('click', view_budget);

function view_budget() {
    console.log("view budget");
    window.location.href = "budget_info.html";
}