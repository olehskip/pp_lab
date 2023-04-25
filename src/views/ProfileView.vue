
<template>
	<div class="profile-container">
		<div class="profile-container-caption">User Profile</div>
		<form>
			<div class="form-group">
				<label for="username">Username:</label>
				<input type="text" id="username" name="username" v-model="username">
			</div>
			<div class="form-group">
				<label for="surname">Surname:</label>
				<input type="text" id="surname" name="surname" v-model="surname">
			</div>
			<div class="form-group">
				<label for="name">Name:</label>
				<input type="text" id="name" name="name" v-model="name">
			</div>
			<div class="form-group">
				<label for="new-password">New Password:</label>
				<input type="password" id="new-password" name="new-password" v-model="password">
			</div>
			<div class="form-group">
				<label for="confirm-password">Confirm Password:</label>
				<input type="password" id="confirm-password" name="confirm-password" v-model="password_repeat">
			</div>
			<div class="buttons-container">
				<button type="button" class="submit-button" @click="send_profile_info">Save</button>
				<button type="button" class="logout-button" @click="logout">Log Out</button>
				<button type="button" class="discard-button" @click="get_profile_info">Discard Changes</button>
				<button type="button" class="delete-button" @click="delete_account">Delete Profile</button>
			</div>
		</form>
		
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
		this.get_profile_info();	
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
		get_profile_info() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
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
		send_profile_info() {
			if(this.$cookies.get('token') == null) {
				this.toast.info("You are not logged in");
				this.$router.push('/login');
			}
			if(this.username.length < 6) {
				this.toast.error("Username must have at least 6 characters");
				return;
			}
			if(this.surname.length < 6) {
				this.toast.error("Surname must have at least 6 characters");
				return;
			}
			if(this.name.length < 6) {
				this.toast.error("Name must have at least 6 characters");
				return;
			}
			if(this.password.length > 0 && this.password.length < 6) {
				this.toast.error("Password must have at least 6 characters");
				return;
			}
			else if(this.password.length > 0 && this.password !== this.password_repeat) {
				this.toast.error("Passwords do not match");
				return;
			}

			const token = this.$cookies.get('token');

			var data = {
				"username": this.username,
				"surname": this.surname,
				"name": this.name,
				"password": this.password
			};

			fetch('/api/user/', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify(data),
            }).then(response => {
				if(response.status == 200) {
					this.toast.success("Profile updated successfully");
				}
				else if(response.status == 403 || response.status == 405) {
					this.toast.error("You are not authorized to update profile");
					this.$cookies.remove('token');
					this.$router.push('/login');
				}
				else {
					this.toast.error("Error updating profile");
				}
			});
		},
		logout() {
			this.$cookies.remove('token');
			this.$router.push('/login');
		},
		delete_account() {
            var token = this.$cookies.get('token');
            fetch('/api/user/', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token
                },
            }).then(response => 
            {
                if(response.status == 200){
					this.toast.warning("Profile deleted");
                }
                else {
                    this.toast.error("Something went wrong");
                }
            }).catch(error => {
				console.log(error);
                this.toast.error("Something went wrong");
            });
			this.$cookies.remove('token');
			this.$router.push('/login');
        },
	}
}
</script>

<style lang="scss">
	@use '@/styles/profile.scss'
</style>
