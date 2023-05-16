<template>
	<div class="budgets-container">
		<div class="budgets-container-header">
			<div class="caption">Your budgets</div>
			<div class="buttons-container">
				<button class="create-budget-button">New personal budget</button>
				<button class="create-budget-button">New family budget</button>
				<button class="view-budget-button" id="view-budget-button">View budget</button>
				<button class="delete-budget-button" id="delete-budget-button">Delete budget</button>
			</div>
		</div>

		<table class="budgets-table" id="budgets-table">
			<thead>
				<tr>
				<td><input type="checkbox" class="chk"></td>
				<th scope="col">ID</th>
				<th scope="col">Type</th>
				<th scope="col">Money</th>
				<th scope="col">Members</th>	
				</tr>
			</thead>
			<tbody>
				<tr v-for="budget in budgets" :key="budget.id">
					<td><input type="checkbox" class="chk"></td>
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
			"budgets": []
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
			fetch('/api/user/budgets', {
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
