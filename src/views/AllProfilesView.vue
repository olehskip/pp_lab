<template>
	<div class='users-container'>
		<div class='users-caption'>All users</div>
		<table class='users-list' id='users-list'>
			<thead>
				<tr>
					<th>User's Name</th>
					<th>Action</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>John Doe</td>
					<td>
						<button class='budgets-button'>Budgets</button>
						<button class='edit-button'>Edit</button>
						<button class='delete-button'>Delete</button>
					</td>
				</tr>
				<tr>
					<td>John Doe</td>
					<td>
						<button class='budgets-button'>Budgets</button>
						<button class='edit-button'>Edit</button>
						<button class='delete-button'>Delete</button>
					</td>
				</tr>
				<tr>
					<td>John Doe</td>
					<td>
						<button class='budgets-button'>Budgets</button>
						<button class='edit-button'>Edit</button>
						<button class='delete-button'>Delete</button>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template> 	

<style lang="scss">
    @use '@/styles/all_profiles.scss'
</style>
