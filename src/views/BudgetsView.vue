<template>
	<div class="budgets-container">
		<div class="budgets-container-header">
			<div class="caption">Your budgets</div>
			<div class="buttons-container">
				<button class="create-budget-button" @click="create_family_budget()">New family budget</button>
			</div>
		</div>

		<table class="budgets-table" id="budgets-table">
			<thead>
				<tr>
				<td></td>
				<th scope="col">ID</th>
				<th scope="col">Type</th>
				<th scope="col">Money</th>
				<th scope="col">Members</th>	
				</tr>
			</thead>
			<tbody>
				<tr v-for="budget in budgets" :key="budget.id" v-on:dblclick="view_budget(budget.type, budget.id)">
					<td></td>
					<td data-label="ID: " scope="row">{{budget.id}}</td>
					<td data-label="Type: ">{{budget.type}}</td>
					<td data-label="Money: ">{{budget.money}}</td>
					<td data-label="Members: ">{{budget.members}}</td>
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
			"budgets": [],
			"checked_budgets": [],
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
			let url = '/api/budgets';
			if(this.$route.params.id) {
				url += '/' + this.$route.params.id;
			}
			fetch(url, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
				},
			}).then(response => {
				if(response.status == 200) {
					response.json().then(data => {
						for(var budget of data) {
							this.budgets.push({
								"id": budget.id,
								"type": budget.type,
								"money": budget.money_amount,
								"members": budget.members.join(", ")
							});
						}
					});
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
				}
				else if(response.status == 404) {
					this.toast.info("Budget not found");
					this.$router.push('/');
				}
				else {
					this.toast.error("Something went wrong");
					this.$cookies.remove('token');
					this.$router.push('/login');
				}
			});
		},
		view_budget(type, id) {
			this.$router.push('/budget/' + type + '/' + id);
		},
		create_family_budget() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}

			var token = this.$cookies.get('token');
			fetch('/api/family_budget', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
				},
			}).then(response => {
				if(response.status == 200) {
					response.json().then(data => {
						this.toast.success("Family budget created");
						this.$router.push('/budget/family/' + data.family_budget_id);
					});
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
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
	@use '@/styles/budgets.scss'
</style>
