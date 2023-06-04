<template>
	<div class='users-container'>
		<div class='users-caption'>All users</div>
		<table class='users-list' id='users-list'>
			<thead>
				<tr>
					<th>User's Name</th>
					<th>Action</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="profile in profiles" :key="profile.username">
					<td>{{profile.username }}</td>
					<td>
						<button class='budgets-button' @click="view_budgets(profile.username)">Budgets</button>
						<button class='delete-button' v-on:click="delete_profile(profile.username)">Delete</button>
					</td>
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
		this.get_profiles();
	},
	data() {
		return {
			"profiles": []
		}
	},
	methods: {
		get_profiles() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}
		
			var token = this.$cookies.get('token');
			fetch('/api/user/all', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
				},
			}).then(response => {
				if(response.status == 200) {
					response.json().then(data => {
						for(let curr of data) {
							this.profiles.push({"username": curr.username});
						}
					});
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
				}
				else if(response.status == 403 || response == 405) {
					this.toast.error("You are not allowed to do this");
					this.$router.push('/');
				}
				else {
					this.toast.error("Something went wrong");
					this.$cookies.remove('token');
					this.$router.push('/login');
				}
			});
		},
		delete_profile(username) {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
				return;
			}

			var token = this.$cookies.get('token');
			
			let data = {
				"username": username
			}

			fetch('/api/user/all', {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
				},
				body: JSON.stringify(data)
			}).then(response => {
				if(response.status == 204) {
					this.toast.success("Profile deleted");
					this.profiles = this.profiles.filter(profile => profile.username != username);
				}
				else if(response.status == 401) {
					this.toast.info("Session exprired");
					this.$router.push('/login');
					this.$cookies.remove('token');
				}
				else if(response.status == 403 || response == 405) {
					this.toast.error("You are not allowed to do this");
				}
				else {
					this.toast.error("Something went wrong");
					this.$cookies.remove('token');
					this.$router.push('/login');
				}
			});
		},
		view_budgets(username) {
			this.$router.push('/budgets/' + username);
		}
	}
}
</script>

<style lang="scss">
    @use '@/styles/all_profiles.scss'
</style>
