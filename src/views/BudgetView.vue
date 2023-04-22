<template>
    <div class="budget-info-container">
        <div class="info-header">
            <div class="budget-info">Budget Information</div>
            <div class="buttons-container">
                <!-- <button class="show-report-button" id="show-report-button">Show Report</button> -->
                <button class="transfer-money-button" id="transfer-money-button">Transfer money</button>
                <button class="delete-button">Delete budget</button>
            </div>
        </div>
        <div class="item">
            <label for="id">ID:</label>
            <input type="text" id="id" value="1312312312" readonly />
        </div>
        <div class="item">
            <label for="type">Type:</label>
            <input type="text" id="type" readonly />
        </div>
        <div class="item">
            <label for="money">Money:</label>
            <input type="text" id="money_amount" readonly />
        </div>
        <hr/>
        <div class="new-member-container">
            <div class="new-member-header">
                <div class="new-member-caption">Add new member</div>
                <button class="new-member-button">Add member</button>
            </div>
            <input type="text" class="new-member-input" placeholder="Username" />
        </div>
        <hr/>
        <table class="list">
            <thead>
                <tr>
                    <th>User's Name</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>John Doe</td>
                    <td><button class="delete-button">Delete</button></td>
                </tr>
                <tr>
                    <td>Jane Doe</td>
                    <td><button class="delete-button">Delete</button></td>
                </tr>
                <tr>
                    <td>Bob Smith</td>
                    <td><button class="delete-button">Delete</button></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style lang="scss">
    @use '@/styles/budget.scss'
</style>
