load_profile();

function load_profile() {
    fetch('/api/user/3').then(response =>
        response.json() ).then(data =>{
            document.getElementById('username').value = data['username'];
            document.getElementById('surname').value = data['surname'];
            document.getElementById('name').value = data['name'];
        });
}