<template>
    <div class="register-container">
        <form name="register-form">
            <div class="form-header">Register to control your budgets effectively</div>
            <label for="surname">Surname</label>
            <input id="surname" name="surname" required placeholder="Your surname">
            <label for="name">Name</label>
            <input id="name" name="name" required placeholder="Your name">
            <label for="username">Username</label>
            <input id="username" name="username" required placeholder="Must have at least 6 characters"/>
            <label for="password">Password</label>
            <input type="password" id="password" name="password" placeholder = "Must have at least 6 characters" required>
            <label for="password">Confirm password</label>
            <input type="password" id="confirm-password" name="password" placeholder = "Must have at least 6 characters" required>
            <button type="submit" class="form-submit-button">Register</button>
        </form>
        
        <div class="right-part"></div>
    </div>
		
		
</template>


<style lang="scss">
    @use '@/styles/register.scss';
</style> 