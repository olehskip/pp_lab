<template>
    <div class="container">
        <div class="form-caption">Money Transfer</div>
        <form class="transfer-money-form">
        <div class="form-group">
            <label for="from-budget">From Budget</label>
            <select id="from-budget" name="from-budget" class="budget-selector" v-model="first_budget_type" >
                <option value="" disabled selected hidden>Budget type</option>
                <option value="personal">Personal</option>
                <option value="family">Family</option>
            </select>
            <input type="number" class="money-amount-selector" id="amount" name="amount" min="0" step="1" placeholder="0" v-model="first_budget_id">
        </div>
        <div class="form-group">
            <label for="to-budget">To Budget</label>
            <select id="from-budget" name="from-budget" class="budget-selector" v-model="second_budget_type">
                <option value="" disabled selected hidden>Budget type</option>
                <option value="personal">Personal</option>
                <option value="family">Family</option>
            </select>
            <input type="number" class="money-amount-selector" id="amount" name="amount" min="0" step="1" placeholder="0" v-model="second_budget_id">
        </div>
        <div class="form-group">
            <label for="amount">Amount</label>
            <input type="number" class="money-amount-selector" id="amount" name="amount" min="0" step="1" placeholder="0" v-model="amount">
        </div>
        <div class="form-group">
            <button type="button" class="submit-button" @click="send_transfer_money()">Transfer</button>
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
	},
	data() {
		return {
			"first_budget_id": "",
            "first_budget_type": "",
            "second_budget_id": "",
            "second_budget_type": "",
            "amount": ""
		}
	},
	methods: {
        send_transfer_money() {
            if(this.$cookies.get('token') == null) {
                this.toast.info("You are not logged in");
                this.$router.push('/login');
                return;
            }

            var token = this.$cookies.get('token');
            let data = {
                "from_budget_id": this.first_budget_id,
                "from_budget_type": this.first_budget_type,
                "to_budget_id": this.second_budget_id,
                "to_budget_type": this.second_budget_type,
                "money_amount": this.amount
            };
            
            fetch("/api/budgets/transfer_money", {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + token,
				},
				body: JSON.stringify(data)
			}).then(response => {
				if(response.status == 204) {
					this.toast.success("Success");
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
                else if(response.status == 404) {
                    this.toast.error("Budget not found");
                }
				else if(response.status == 400) {
					response.json().then(response => {
                        console.log(response);
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
    @use '@/styles/transfer_money.scss'
</style>
