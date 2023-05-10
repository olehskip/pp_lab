<template>
    <div class="budget-info-container">
        <div class="info-header">
            <div class="budget-info">Budget Information</div>
            <div class="buttons-container">
                <!-- <button class="show-report-button" id="show-report-button">Show Report</button> -->
                <button class="transfer-money-button" id="transfer-money-button">Transfer money</button>
                <button class="delete-button">Delete budget</button>
            </div>
        </div>
        <div class="item">
            <label for="id">ID:</label>
            <input type="text" id="id" value="1312312312" readonly />
        </div>
        <div class="item">
            <label for="type">Type:</label>
            <input type="text" id="type" readonly />
        </div>
        <div class="item">
            <label for="money">Money:</label>
            <input type="text" id="money_amount" readonly />
        </div>
        <hr/>
        <div class="new-member-container">
            <div class="new-member-header">
                <div class="new-member-caption">Add new member</div>
                <button class="new-member-button">Add member</button>
            </div>
            <input type="text" class="new-member-input" placeholder="Username" />
        </div>
        <hr/>
        <table class="list">
            <thead>
                <tr>
                    <th>User's Name</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>John Doe</td>
                    <td><button class="delete-button">Delete</button></td>
                </tr>
                <tr>
                    <td>Jane Doe</td>
                    <td><button class="delete-button">Delete</button></td>
                </tr>
                <tr>
                    <td>Bob Smith</td>
                    <td><button class="delete-button">Delete</button></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
	setup() {
		let toast = useToast();
		return { toast }
	},
	beforeMount() {
		this.get_budgets();	
	},
	data() {
		return {
			"username": "",
			"surname": "",
			"name": "",
			"password": "",
			"password_repeat": ""
		}
	},
	methods: {
		get_budgets() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}
		
			var token = this.$cookies.get('token');
			fetch('/api/user/', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
				},
			}).then(response => {
				if (response.status == 403 || response.status == 405) {
					this.toast.error("You are not authorized to view this profile");
					this.$cookies.remove('token');
					this.$router.push('/login');
				}
				else if(response.status == 200) {
					response.json().then(data => {
						console.log(data)
						this.username = data.username;
						this.surname = data.surname;
						this.name = data.name;
						this.password = "";
						this.password_repeat = "";
					});
				}
				else {
					this.toast.error("Something went wrong");
					this.$cookies.remove('token');
					this.$router.push('/login');
				}
			});
		},
	}
}
</script>

<style lang="scss">
    @use '@/styles/budget.scss'
</style>
