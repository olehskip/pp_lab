<template>
    <div class="register-container">
        <form name="register-form">
            <div class="form-header">Register to control your budgets effectively</div>
            <label for="surname">Surname</label>
            <input id="surname" name="surname" required placeholder="Your surname" v-model="surname">
            
            <label for="name">Name</label>
            <input id="name" name="name" required placeholder="Your name" v-model="name">
            
            <label for="username">Username</label>
            <input id="username" name="username" v-model="username" required placeholder="Must have at least 6 characters"/>
            
            <label for="password">Password</label>
            <input type="password" id="password" name="password" v-model="password" placeholder = "Must have at least 6 characters" required>
            
            <label for="password">Confirm password</label>
            <input type="password" id="confirm-password" name="password" v-model="password_repeat" placeholder = "Must have at least 6 characters" required>
            <div class="form-link">
                <router-link to="/login">Already have an account?</router-link>
            </div>
            <button type="button" class="form-submit-button" @click="send_register">Register</button>
        </form>
        
        <div class="right-part"></div>
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
        if(this.$cookies.get('token') != null) {
			this.toast.info("You are already registered");
            this.$router.push('/');
        }
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
		send_register() {
            var is_data_valid = true;

			if(this.username.length < 6) {
                this.toast.error("Username must have at least 6 characters");
                is_data_valid = false;
            }
            if(this.surname.length < 6) {
                this.toast.error("Surname must have at least 6 characters");
                is_data_valid = false;
            }
            if(this.name.length < 6) {
                is_data_valid = false;
                this.toast.error("Name must have at least 6 characters");
            }
            if(this.password.length < 6) {
                is_data_valid = false;
                this.toast.error("Password must have at least 6 characters");
            }
            else if(this.password_repeat != this.password) {
                this.toast.error("Passwords do not match");
                is_data_valid = false;
            }
            if(is_data_valid == false) {
                return;
            }

            let data = {
                "username": this.username,
                "surname": this.surname,
                "name": this.name,
                "password": this.password
            }
            fetch('/api/user/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            }).then(response => 
            {
                if(response.status == 409) {
                    this.toast.error("Username already exists");
                }
                else if(response.status == 400) {
                    this.toast.error("Invalid data");
                }
                else if(response.status == 200){
                    response.json().then(response => {
                        this.toast.clear();
                        this.$cookies.set('token', response.token, '15min');
                        this.$router.push('/');
                    }).catch(error => {
                        console.log(error);
                        this.toast.error("Error");
                    });
                }
            }).catch(error => {
                console.log(error);
                this.toast.error("Error");
            });
		},
	}
}
</script>

<style lang="scss">
    @use '@/styles/register.scss';
</style> 