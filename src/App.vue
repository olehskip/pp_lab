<template>
	<header class="header" v-if="toShowHeader">
		<nav>
			<ul>
				<li><router-link to="/profile">Profile</router-link></li> |
				<li><router-link to="/budgets">Budgets</router-link></li> |
				<li><router-link to="/transfer_money">Transfer Money</router-link></li> |
				<li><router-link to="/all_profiles">All profiles</router-link></li>
			</ul>
		</nav>
	</header>
	<router-view/>
</template>

<script>
export default {
	computed: {
		toShowHeader() {
			return this.$route.path !== '/register' && this.$route.path !== '/login';
		}
	}
}
</script>

<style lang="scss">
	@use "@/styles/header.scss";

</style>
