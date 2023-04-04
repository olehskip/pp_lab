// Get the form element
const register_form = document.getElementsByName('register-form')[0];

register_form.addEventListener('submit', (event) => {
	event.preventDefault();

	const formData = new FormData(register_form);
	const data = Object.fromEntries(formData.entries());

	const formJsonData = JSON.stringify(data);
	console.log(formJsonData);

	jsonData = JSON.stringify({
		"username": data.username,
		"surname": data.surname,
		"name": data.name,
		"password": data.password,
	})
	fetch('/user', {
		method: 'POST',
		headers: {
		'Content-Type': 'application/json'
		},
		body: jsonData
	})
	.then(response => response.json())
	.then(data => {
		// Handle the response from the server
	})
	.catch(error => {
		// Handle any errors that occur during the request
	});

	return false;
});
