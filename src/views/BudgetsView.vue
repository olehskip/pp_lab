<template>
    <div class="budgets-container">
		<div class="budgets-container-header">
			<div class="caption">Your budgets</div>
			<div class="buttons-container">
				<button class="create-budget-button">New personal budget</button>
				<button class="create-budget-button">New family budget</button>
				<button class="view-budget-button" id="view-budget-button">View budget</button>
				<button class="delete-budget-button" id="delete-budget-button">Delete budget</button>
			</div>
		</div>

		<table class="budgets-table" id="budgets-table">
			<thead>
				<tr>
				<td><input type="checkbox" class="chk"></td>
				<th scope="col">ID</th>
				<th scope="col">Type</th>
				<th scope="col">Money</th>
				<th scope="col">Members</th>	
				</tr>
			</thead>
			<tbody>
				<tr>
				<td><input type="checkbox" class="chk"></td>
				<td data-label="ID: " scope="row">1232131234</td>
				<td data-label="Type: ">Family</td>
				<td data-label="Money: ">134312$</td>
				<td data-label="Members: ">ASFdfdsf sdjsdf sdjlf dsf sdf jdslfdsfjdslfdsf</td>
				</tr>
				<tr>
				<td><input type="checkbox" class="chk"></td>
				<td data-label="ID: " scope="row">1232131234</td>
				<td data-label="Type: ">Family</td>
				<td data-label="Money: ">134312$</td>
				<td data-label="Members: ">ASFdfdsf sdjsdf sdjlf dsf sdf jdslfdsfjdslfdsf</td>
				</tr>

				<tr>
				<td><input type="checkbox" class="chk"></td>
				<td data-label="ID: " scope="row">1232131234</td>
				<td data-label="Type: ">Family</td>
				<td data-label="Money: ">134312$</td>
				<td data-label="Members: ">ASFdfdsf sdjsdf sdjlf dsf sdf jdslfdsfjdslfdsf</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<style lang="scss">
    @use '@/styles/budgets.scss'
</style>
