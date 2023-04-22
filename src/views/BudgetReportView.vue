<template>
    <div class="report-info-container">
        <div class="info-header">
            <div class="report-info">Budget report</div>
        </div>
        <div class="item">
            <label for="id">ID:</label>
            <input type="text" id="id" value="1312312312" readonly />
        </div>
        <hr/>
        <table class="report-table">
            <thead>
                <tr>
                    <th scope="col">From budget</th>
                    <th scope="col">To budget</th>
                    <th scope="col">Sender</th>
                    <th scope="col">Money</th>
                    <th scope="col">Time</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td data-label="From budget: " scope="row">1232131234</td>
                    <td data-label="To budget: ">123123123</td>
                    <td data-label="Sender: ">1235345345</td>
                    <td data-label="Money: ">134312$</td>
                    <td data-label="Time: ">Today, 14:35</td>
                </tr>
                <tr>
                    <td data-label="From budget: " scope="row">1232131234</td>
                    <td data-label="To budget: ">123123123</td>
                    <td data-label="Sender: ">1235345345</td>
                    <td data-label="Money: ">134312$</td>
                    <td data-label="Time: ">Today, 14:35</td>
                </tr>
                <tr>
                    <td data-label="From budget: " scope="row">1232131234</td>
                    <td data-label="To budget: ">123123123</td>
                    <td data-label="Sender: ">1235345345</td>
                    <td data-label="Money: ">134312$</td>
                    <td data-label="Time: ">Today, 14:35</td>
                </tr>
                <tr>
                    <td data-label="From budget: " scope="row">1232131234</td>
                    <td data-label="To budget: ">123123123</td>
                    <td data-label="Sender: ">1235345345</td>
                    <td data-label="Money: ">134312$</td>
                    <td data-label="Time: ">Today, 14:35</td>
                </tr>
                <tr>
                    <td data-label="From budget: " scope="row">1232131234</td>
                    <td data-label="To budget: ">123123123</td>
                    <td data-label="Sender: ">1235345345</td>
                    <td data-label="Money: ">134312$</td>
                    <td data-label="Time: ">Today, 14:35</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style lang="scss">
    @use '@/styles/budget_report.scss'
</style>
