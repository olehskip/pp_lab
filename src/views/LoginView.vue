<template>
    <div class="login-container">
        <form>
            <div class="form-header">Log in to have full access to your budgets</div>
            
            <label for="username">Username</label>
            <input id="username" name="username" v-model="username" required placeholder="Your username">
            
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" name="password" placeholder = "Must have at least 6 characters" required>
            <div class="form-link">
                <router-link to="/register">Don't have an account?</router-link>
            </div>
            <button type="button" @click="send_login" class="form-submit-button">Log In</button>
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
			this.toast.info("You are already logged in");
            this.$router.push('/');
        }
	},
	data() {
		return {
			"surname": "",
			"password": ""
		}
	},
    methods: {
		send_login() {
            var is_data_valid = true;
            if(this.username.length < 6) {
                this.toast.error("Username must have at least 6 characters");
                is_data_valid = false;
            }
            if(this.password.length < 6) {
                this.toast.error("Password must have at least 6 characters");
                is_data_valid = false;
            }
            
            if(!is_data_valid) {
                return;
            }


            let data = {
                "username": this.username,
                "password": this.password
            }
            fetch('/api/user/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
            }).then(response => 
            {
                if(response.status == 404) {
                    this.toast.error("Username not found");
                }
                else if(response.status == 401) {
                    this.toast.error("Invalid password")
                }
                else if(response.status == 200) {
                    response.json().then(response => 
                    {
                        this.toast.clear();
                        this.$cookies.set('token', response.token, '15min');
                        this.$router.push('/');
                    }).catch(error => 
                    {
                        console.log(error);
                        this.toast.error("Error");
                    });
                }
                else {
                    this.toast.error("Error");
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
    @use '@/styles/login.scss';
</style>