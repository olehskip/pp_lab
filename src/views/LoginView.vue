<template>
    <div class="login-container">
        <form>
            <div class="form-header">Log in to have full access to your budgets</div>
            
            <label for="username_input">Username</label>
            <input id="username_input" name="username_input" v-model="username" required placeholder="Your username">
            
            <label for="password_input">Password</label>
            <input type="password" id="password_input" v-model="password" name="password" placeholder = "Must have at least 6 characters" required>
            <div class="form-link">
                <router-link to="/register">Don't have an account?</router-link>
            </div>
            <button type="button" @click="send_login" class="form-submit-button" id="form_button">Log In</button>
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
			"username": "",
			"password": ""
		}
	},
    methods: {
		send_login() {
            var is_data_valid = true;
            if(!this.username || this.username.length == 0) {
                is_data_valid = false;
            }
            if(this.password == null || this.password.length == 0) {
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
                        this.toast.error("Error");
                    });
                }
                else if(response.status == 400) {
                    for (var key in response) {
                        var val = response[key];
                        this.toast.error(key + ": " + val);
                    }
                }
                else {
                    this.toast.error("Error");
                }
            }).catch(error => {
                this.toast.error("Error");
            });
		}
	}
}
</script>

<style lang="scss">
    @use '@/styles/login.scss';
</style>