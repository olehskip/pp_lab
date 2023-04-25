import { createRouter, createWebHistory } from 'vue-router'

const routes = [
	{
		path: '/all_profiles',
		name: 'all_profiles',
		component: () => import('@/views/AllProfilesView.vue')
	},
	{
		path: '/budget',
		name: 'budget',
		component: () => import('@/views/BudgetView.vue')
	},
	{
		path: '/budgets',
		name: 'budgets',
		component: () => import('@/views/BudgetsView.vue')
	},
	{
		path: '/budget_report',
		name: 'budget_report',
		component: () => import('@/views/BudgetReportView.vue')
	},
	{
		path: '/error',
		name: 'error',
		component: () => import('@/views/ErrorView.vue')
	},
	{
		path: '/login',
		name: 'login',
		component: () => import('@/views/LoginView.vue')
	},
	{
		path: '/',
		alias: '/profile',
		name: 'profile',
		component: () => import('@/views/ProfileView.vue')
	},
	{
		path: '/register',
		name: 'register',
		component: () => import('@/views/RegisterView.vue')
	},
	{
		path: '/transfer_money',
		name: 'transfer_money',
		component: () => import('@/views/TransferMoneyView.vue')
	}
]
	
const router = createRouter({
	history: createWebHistory(),
	routes
})

export default router
