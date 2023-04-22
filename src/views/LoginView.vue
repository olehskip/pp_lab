<template>
    <div class="login-container">
        <form>
            <div class="form-header">Log in to have full access to your budgets</div>
            <label for="username">Username</label>
            <input id="username" name="username" required placeholder="Your username">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" placeholder = "Must have at least 6 characters" required>
            <div class="form-link">
                <a href="#">Don"t have an account?</a>
            </div>
            <button type="submit" class="form-submit-button">Log In</button>
        </form>
        
        <div class="right-part"></div>
	</div>
</template>

<style lang="scss">
    @use '@/styles/login.scss';
</style>