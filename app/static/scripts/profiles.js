load_profiles();

function load_profiles() {
    fetch('/api/user').then(response =>
        response.json() ).then(data =>{
            table = document.getElementById('users-list');
            cells = table.tBodies[0].rows[0].cells;
            cells[0].innerText = data[0]['username'];

            cells = table.tBodies[0].rows[1].cells;
            cells[0].innerText = data[1]['username'];
        });
}