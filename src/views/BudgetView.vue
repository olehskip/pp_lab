<template>
	<div class="budget-info-container">
		<div class="info-header">
			<div class="budget-info">Budget Information</div>
			<div class="buttons-container">
				<!-- <button class="show-report-button" id="show-report-button">Show Report</button> -->
				<button class="transfer-money-button" id="transfer-money-button">Transfer money</button>
				<button class="delete-button" v-if="budget_type=='family'" @click="delete_budget">Delete budget</button>
			</div>
		</div>
		<div class="item">
			<label for="id">ID:</label>
			<input type="text" id="id" :value="budget_id" readonly />
		</div>
		<div class="item">
			<label for="type">Type:</label>
			<input type="text" id="type" :value="budget_type" readonly />
		</div>
		<div class="item">
			<label for="money">Money:</label>
			<input type="text" id="money_amount" :value="budget_money + ' $'" readonly />
		</div>
		<div class="new-member-container" v-if="budget_type=='family'">
			<hr/>
			<div class="new-member-header">
				<div class="new-member-caption">Add a new member</div>
				<button class="new-member-button" @click="add_new_member">Add a member</button>
			</div>
			<input type="text" class="new-member-input" placeholder="Username" v-model="new_member_username"/>
		</div>
		<table class="list" v-if="budget_type=='family'">
			<thead>
				<tr>
					<th>User's Name</th>
					<th>Action</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="member in budget_members" :key="member.username">
					<td>{{member.username}}</td>
					<td><button class="delete-button" v-on:click="delete_member(member.username)">Delete</button></td>
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
		this.get_budget();	
	},
	data() {
		return {
			"budget_id": "",
			"budget_type": "",
			"budget_money": "",
			"budget_members": [],
			"new_member_username": ""
		}
	},
	methods: {
		get_budget() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}
			var token = this.$cookies.get('token');
			var budget_id = this.$route.params.id;
			
			var fetch_url = '';
			if (this.$route.params.type == 'family') {
				fetch_url = '/api/family_budget/';
			}
			else if (this.$route.params.type == 'personal') {
				fetch_url = '/api/personal_budget/';
			}
			else {
				this.toast.error("Not found");
				this.$router.push('/');
				return;
			}
			fetch(fetch_url + budget_id.toString(), {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
				}
			}).then(response => {
				if(response.status == 200) {
					response.json().then(response => {
						this.budget_id = response.id;
						this.budget_type = response.type;
						this.budget_money = response.money;
						for(var member of response.members) {
							this.budget_members.push({username: member});
						}
					}).catch(error => {
						console.log(error);
						this.toast.error("Error");
					});
				}
				else if(response.status == 403 || response.status == 405) {
					this.toast.error("You are not authorized to view this budget");
					this.$router.push('/');
				}
				else if(response.status == 400) {
					response.json().then(response => {
						for (var key in response) {
							var val = response[key];
							this.toast.error(key + ": " + val);
						}
					}).catch(error => {
						console.log(error);
						this.toast.error("Error");
						this.$
					});
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
				}
				else {
					this.toast.error("Error");
					this.$router.push('/');
				}
			});
		},
		delete_budget() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}
			var token = this.$cookies.get('token');
			var budget_id = this.$route.params.id;
			var budget_type = this.$route.params.type;
			if(budget_type == 'personal') {
				this.toast.error("You can't delete a personal budget");
				return;
			}

			fetch("/api/family_budget/" + budget_id.toString(), {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
				}
			}).then(response => {
				if(response.status == 200) {
					this.toast.success("Budget deleted");
					this.$router.push('/');
				}
				else if(response.status == 403 || response.status == 405) {
					this.toast.error("You are not authorized to delete this budget");
					this.$router.push('/');
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
				}
				else {
					this.toast.error("Error");
					this.$router.push('/');
				}
			});
		},
		add_new_member() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}

			var token = this.$cookies.get('token');
			var budget_id = this.$route.params.id;
			var budget_type = this.$route.params.type;
			if(budget_type == 'personal') {
				this.toast.error("You can't add a member to a personal budget");
				return;
			}
			var username = this.new_member_username;
			if(username == "") {
				this.toast.error("Username can't be empty");
				return;
			}

			var data = {
				"username": username
			}
			fetch("/api/family_budget/" + budget_id.toString() + "/add_member", {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token,
				},
				body: JSON.stringify(data)
			}).then(response => {
				if(response.status == 204) {
					this.toast.success("Added new member");
					this.budget_members.push({username: username});
					this.new_member_username = "";
				}
				else if(response.status == 403 || response.status == 405) {
					this.toast.error("You are not authorized to change this budget");
					this.$router.push('/');
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
				}
				else if(response.status == 400) {
					response.json().then(response => {
						this.toast.error(response.error);
					}).catch(error => {
						console.log(error);
						this.toast.error("Error");
					});
				}
				else {
					this.toast.error("Error");
					this.$router.push('/');
				}
			});
		},
		delete_member(username_to_delete)
		{
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}

			var token = this.$cookies.get('token');
			var budget_id = this.$route.params.id;
			var budget_type = this.$route.params.type;

			if(budget_type == 'personal') {
				this.toast.error("You can't delete a member from a personal budget");
				return;
			}

			var data = {
				"username": username_to_delete
			}

			fetch("/api/family_budget/" + budget_id + "/delete_member", {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token,
				},
				body: JSON.stringify(data)
			}).then(response => {
				if(response.status == 204) {
					this.toast.success("The member was deleted");
					this.budget_members = this.budget_members.filter(member => member.username != username_to_delete);
				}
				else if(response.status == 403 || response.status == 405) {
					this.toast.error("You are not authorized to change this budget");
					this.$router.push('/');
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
				}
				else if(response.status == 400) {
					response.json().then(response => {
						this.toast.error(response.error);
					}).catch(error => {
						console.log(error);
						this.toast.error("Error");
					});
				}
				else {
					this.toast.error("Error");
					this.$router.push('/');
				}
			});
		}
	}
}
</script>

<style lang="scss">
	@use '@/styles/budget.scss'
</style>
