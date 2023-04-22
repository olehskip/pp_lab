<template>
    <div class="container">
        <div class="form-caption">Money Transfer</div>
        <form class="transfer-money-form">
        <div class="form-group">
            <label for="from-budget">From Budget</label>
            <select id="from-budget" name="from-budget" class="budget-selector">
                <option value="budget1">Budget 1</option>
                <option value="budget2">Budget 2</option>
                <option value="budget3">Budget 3</option>
            </select>
        </div>
        <div class="form-group">
            <label for="to-budget">To Budget</label>
            <select id="to-budget" name="to-budget" class="budget-selector">
                <option value="budget1">Budget 1</option>
                <option value="budget2">Budget 2</option>
                <option value="budget3">Budget 3</option>
            </select>
        </div>
        <div class="form-group">
            <label for="amount">Amount</label>
            <input type="number" class="money-amount-selector" id="amount" name="amount" min="0" step="0.01" placeholder="0.00">
        </div>
        <div class="form-group">
            <button type="submit" class="submit-button">Transfer</button>
        </div>
        </form>
    </div>
</template>

<style lang="scss">
    @use '@/styles/transfer_money.scss'
</style>
