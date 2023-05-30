import { shallowMount, mount } from '@vue/test-utils';
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import BudgetView from '@/views/BudgetView.vue'
import ErrorView from '@/views/ErrorView.vue'
import TransferMoneyView from '@/views/TransferMoneyView.vue'
import AllProfilesView from '@/views/AllProfilesView.vue'
import BudgetsView from '@/views/BudgetsView.vue'
import ProfileView from '@/views/ProfileView.vue'
import VueToastificationPlugin from "vue-toastification";
import router from '@/router';

require('jest-fetch-mock').enableMocks()

const mockRouter = {
	push: jest.fn()
}

const mockToast = {
	success: jest.fn(),
	error: jest.fn(),
	info: jest.fn(),
	clear: jest.fn()
};

beforeEach(() => {
	fetch.resetMocks();
});
describe('LoginView.vue', () => {
	let wrapper;
	beforeEach(() => {
		wrapper = mount(LoginView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn(),
					},
				},
			}
		});
	});
	it('should not submit when data is empty', async () => {
		wrapper.find('button').trigger('click');
		expect(fetchMock).not.toHaveBeenCalled();
	});
	it("should not submit when password is empty", async () => {
		wrapper.vm.username = "test1";
		wrapper.find('button').trigger('click');
		expect(fetchMock).not.toHaveBeenCalled();
	});
	it("should sumbit", async () => {
		fetch.mockResponse(JSON.stringify({}));
		wrapper.vm.username = "test1";
		wrapper.vm.password = "test";
		wrapper.find('#form_button').trigger('click');
		expect(fetchMock).toHaveBeenCalled();
	});
	it("fetch should catch error", async () => {
		fetch.mockReject(() => Promise.reject("API is down"));
		wrapper.vm.username = "test1";
		wrapper.vm.password = "test";
		wrapper.find('#form_button').trigger('click');
		expect(fetchMock).toHaveBeenCalled();
	});
	it("fetch response is 404", async () => {
		fetch.mockResponse(JSON.stringify({}), { status: 404 });
		wrapper.vm.username = "test1";
		wrapper.vm.password = "test";
		wrapper.find('#form_button').trigger('click');
		expect(fetchMock).toHaveBeenCalled();
	});
	it("fetch response is 200", async () => {
		fetch.mockResponse(JSON.stringify({}), { status: 200 });
		wrapper.vm.username = "test1";
		wrapper.vm.password = "test";
		wrapper.find('#form_button').trigger('click');
		expect(fetchMock).toHaveBeenCalled();
	});
	it("fetch response is 401", async () => {
		fetch.mockResponse(JSON.stringify({}), { status: 401 });
		wrapper.vm.username = "test1";
		wrapper.vm.password = "test";
		wrapper.find('#form_button').trigger('click');
		expect(fetchMock).toHaveBeenCalled();
	});
});

describe('LoginView.vue', () => {

	it("should be routed if token in cookies", async () => {
		const wrapper = mount(LoginView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue("very cool token"),
					},
					$router: mockRouter
				},
			}
		});
		expect(mockRouter.push).toHaveBeenCalled()
	});
});

describe('RegisterView.vue', () => {
	let wrapper;
	beforeEach(() => {
		wrapper = mount(RegisterView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn(),
						set: jest.fn()
					}
				},
			}
		});
	});

	it('should not submit when data is empty', async () => {
		wrapper.find('button').trigger('click');
		expect(fetchMock).not.toHaveBeenCalled();
	});
	it("should not submit when password repeat length 0", async () => {
		wrapper.vm.password = "test";
		wrapper.vm.password_repeat = "";
		wrapper.find('button').trigger('click');
		expect(fetchMock).not.toHaveBeenCalled();
	});
	it("should not submit if passwords do not match", async () => {
		wrapper.vm.password = "test";
		wrapper.vm.password_repeat = "test1";
		wrapper.find('button').trigger('click');
		expect(fetchMock).not.toHaveBeenCalled();
	});
});

describe('RegisterView.vue', () => {
	let wrapper;
	let cookies = {
		set: jest.fn(),
		get: jest.fn()
	}
	beforeEach(() => {
		wrapper = mount(RegisterView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: cookies,
					toast: mockToast
				},
			}
		});
		wrapper.vm.password = "password";
		wrapper.vm.username = "username";
		wrapper.vm.name = "name";
		wrapper.vm.surname = "surname";
		wrapper.vm.password_repeat = "password";
	});
	it("should submit", async () => {
		fetch.mockResponse(JSON.stringify({}));
		wrapper.find('button').trigger('click');
		expect(fetchMock).toHaveBeenCalled();
	});
	it("fetch should catch error", async () => {
		fetch.mockReject(() => Promise.reject("API is down"));
		wrapper.find('button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
	});
	it("fetch response is 409", async () => {
		fetch.mockResponse(JSON.stringify({}), { status: 409 });
		wrapper.find('button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
	});
	it("fetch response is 200", async () => {
		fetch.mockResponse(JSON.stringify({ "token": "new token" }), { status: 200 });
		wrapper.find('button').trigger('click');
		expect(mockToast.clear).toHaveBeenCalled();
		expect(mockToast.clear).toHaveBeenCalled();
		expect(cookies.set).toHaveBeenCalled();
	});
	it("fetch response is 400", async () => {
		fetch.mockResponse(JSON.stringify({}), { status: 400 });
		wrapper.find('button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
	});
	it("fetch response is 400 but receive bad json", async () => {
		fetch.mockResponse("bad json", { status: 400 });
		wrapper.find('button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
	});
	it("received 400 and error message", async () => {
		fetch.mockResponse(JSON.stringify({ "error": "bad username" }), { status: 400 });
		wrapper.find('button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
	});
});

describe('RegisterView.vue', () => {
	it("should be routed if token in cookies", async () => {
		const wrapper = mount(RegisterView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue("very cool token"),
					},
					$router: mockRouter
				},
			}
		});
		expect(mockRouter.push).toHaveBeenCalledWith("/");
	});
});

describe('BudgetView.vue', () => {
	it("should be routed if type is wrong", async () => {
		let wrapper = mount(BudgetView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue("very cool token"),
					},
					toast: mockToast,
					$router: mockRouter,
					$route: {
						params: {
							type: "family1"
						}
					}
				},
			}
		});
		wrapper.vm.type = "family1";
		expect(mockRouter.push).toHaveBeenCalledWith("/");
		expect(mockToast.error).toHaveBeenCalled();
	});

	it("should be routed in get_budget() if token not in cookies", async () => {
		let wrapper = mount(BudgetView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter
				},
			}
		});
		wrapper.find('button').trigger('click');
		expect(mockToast.info).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/login");
	});

	it("should be routed in delete_budget() if token not in cookies", async () => {
		let wrapper = mount(BudgetView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter
				},
			}
		});
		wrapper.find('#delete-button').trigger('click');
		expect(mockToast.info).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/login");
	});

	it("should be routed in add_new_members() if token not in cookies", async () => {
		let wrapper = mount(BudgetView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter,
					$route: {
						params: {
							type: "family",
							id: 1
						}
					},
				},
			}
		});
		wrapper.vm.new_member_username = "some username";
		wrapper.find('#new-member-button').trigger('click');
		expect(mockToast.info).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/login");
	});

	it("should be routed in delete_member() if token not in cookies", async () => {
		let wrapper = mount(BudgetView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter,
					$route: {
						params: {
							type: "family",
							id: 1
						}
					},
				},
			}
		});
		wrapper.vm.delete_member("some username");
		expect(mockToast.info).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/login");
	});
	
	// it("received 200 get_budget()", async () => {
	// 	let wrapper = mount(BudgetView, {
	// 		global: {
	// 			stubs: ['router-link'],
	// 			mocks: {
	// 				$cookies: {
	// 					get: jest.fn().mockReturnValue("very cool token"),
	// 					set: jest.fn()
	// 				},
	// 				toast: mockToast,
	// 				$router: mockRouter,
	// 				$route: {
	// 					params: {
	// 						type: "personal",
	// 						id: 1
	// 					}
	// 				},
	// 			},
	// 		}
	// 	});
	// 	wrapper.vm.fetch = 
	// 	});
	// 	console.log("START");
	// 	wrapper.vm.get_budget();
	// 	console.log("END");
		
	// 	// expect(wrapper.vm.budget_id).toBe(1);
	// });
});

describe('BudgetView.vue', () => {
	let wrapper;
	beforeEach(() => {
		wrapper = mount(BudgetView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue("very cool token"),
						set: jest.fn()
					},
					toast: mockToast,
					$router: mockRouter,
					$route: {
						params: {
							type: "personal",
							id: 1
						}
					},
					get_budget() { },
				},
			}
		});
	});

	it('cannot delete personal budget', async () => {
		wrapper.vm.type = "personal";
		fetch.resetMocks();
		wrapper.find('#delete-button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
		expect(fetchMock).not.toHaveBeenCalled();
	});

	it('cannot add member to personal budget', async () => {
		wrapper.vm.type = "personal";
		fetch.resetMocks();
		wrapper.vm.new_member_username = "some username";
		wrapper.find('#new-member-button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
		expect(fetchMock).not.toHaveBeenCalled();
	});

	it('cannot delete member from personal budget', async () => {
		wrapper.vm.type = "personal";
		fetch.resetMocks();
		wrapper.vm.delete_member("some username");
		expect(mockToast.error).toHaveBeenCalled();
		expect(fetchMock).not.toHaveBeenCalled();
	});
});

describe('BudgetView.vue', () => {
	let wrapper;
	beforeEach(() => {
		wrapper = mount(BudgetView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue("very cool token"),
						set: jest.fn()
					},
					toast: mockToast,
					$router: mockRouter,
					$route: {
						params: {
							type: "family",
							id: 1
						}
					},
				},
			}
		});
	});

	it("received 400 get_budget()", async () => {
		fetchMock.mockResponse(JSON.stringify({ "error": "bad" }), { status: 400 });
		wrapper.find('button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/");
	});

	it("received 200 get_budget()", async () => {
		fetchMock.mockResponse(JSON.stringify({}), { status: 200 });
		wrapper.find('button').trigger('click');
	});

	it("received 200 delete_budget()", async () => {
		fetchMock.mockResponse(JSON.stringify({}), { status: 200 });
		wrapper.find('#delete-button').trigger('click');
	});

	it("received 204 add_new_members()", async () => {
		fetchMock.mockResponse(JSON.stringify({}), { status: 204 });
		wrapper.vm.new_member_username = "some username";
		wrapper.find('#new-member-button').trigger('click');
		wrapper.vm.$nextTick(() => {
			expect(wrapper.vm.new_member_username).toBe("");
		});
	});

	it("should not submit empty new member add_new_members()", async () => {
		wrapper.vm.new_member_username = "";
		wrapper.find('#new-member-button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
		fetch.resetMocks();
		expect(fetchMock).not.toHaveBeenCalled();
	});

	it("add new_member fetch error", async () => {
		fetch.resetMocks();
		fetch.mockReject(new Error("fake error message"));
		wrapper.find('#new-member-button').trigger('click');
		expect(mockToast.error).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/");
	});

	it('should handle response status 403 correctly add_new_member()', async () => {
		wrapper.vm.fetch = Promise.resolve({
			status: 403,
			json: () => Promise.resolve(),
		});
		wrapper.vm.add_new_member();
		expect(wrapper.vm.toast.error).toHaveBeenCalled();
		expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/');
	});

	it('should handle response status 403 correctly delete_new_member()', async () => {
		wrapper.vm.fetch = Promise.resolve({
			status: 403,
			json: () => Promise.resolve(),
		});
		wrapper.vm.delete_budget();
		expect(wrapper.vm.toast.error).toHaveBeenCalled();
		expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/');
	});

	it("delete member 200", async () => {
		fetchMock.mockResponse(JSON.stringify({}), { status: 204 });
		wrapper.vm.delete_member("some username");
		expect(mockToast.success).toHaveBeenCalled();
	});

	it("delete member 403", async () => {
		wrapper.vm.fetch = Promise.resolve({
			status: 403,
			json: jest.fn().mockReturnValue({}),
		});
		wrapper.vm.delete_member("some username");
		expect(mockToast.error).toHaveBeenCalled();
	});

	it("delete member 401", async () => {
		wrapper.vm.fetch = Promise.resolve({
			status: 401,
			json: jest.fn().mockReturnValue({}),
		});
		wrapper.vm.delete_member("some username");
		expect(mockToast.error).toHaveBeenCalled();
	});

	it("add_new_member fetch error", async () => {
		fetch.resetMocks();
		wrapper.vm.fetch = Promise.resolve({
			status: null,
			json: jest.fn().mockReturnValue({}),
		});
		
		wrapper.vm.add_new_member();
		expect(mockToast.error).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/");
	});
});

describe('ErrorView.vue', () => {
	
	it("should be routed in error()", async () => {
		let wrapper = mount(ErrorView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter
				},
			}
		});
		expect(wrapper.find("img").exists()).toBe(true);
	});
});

describe('TransferMoneyView.vue', () => {
	it("should be routed if no token", async () => {
		let wrapper = mount(TransferMoneyView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter
				},
			}
		});
		wrapper.vm.send_transfer_money();
		expect(mockToast.error).toHaveBeenCalled();
		expect(mockRouter.push).toHaveBeenCalledWith("/");
	});

	it("received 200", async () => {
		let wrapper = mount(TransferMoneyView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue("very cool token"),
					},
					toast: mockToast,
					$router: mockRouter
				},
			}
		});
		fetchMock.mockResponse(JSON.stringify({}), { status: 204 });
		wrapper.vm.send_transfer_money();
		expect(mockToast.success).toHaveBeenCalled();
	});
});

describe('AllProfilesView.vue', () => {
	it("should be routed if no token", async () => {
		let wrapper = mount(AllProfilesView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter
				},
			}
		});
		expect(mockRouter.push).toHaveBeenCalledWith("/");
		expect(mockToast.info).toHaveBeenCalled();
	});
});

describe('BudgetsView.vue', () => {
	it("should be routed if no token", async () => {
		let wrapper = mount(BudgetsView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter,
					$route: {
						params: {
							id: 1
						}
					}
				},
			}
		});
		expect(mockRouter.push).toHaveBeenCalledWith("/");
		expect(mockRouter.push).toHaveBeenCalledWith("/");
	});
});

describe('ProfileView.vue', () => {
	it("should be routed if no token", async () => {
		let wrapper = mount(ProfileView, {
			global: {
				stubs: ['router-link'],
				mocks: {
					$cookies: {
						get: jest.fn().mockReturnValue(null),
					},
					toast: mockToast,
					$router: mockRouter,
					$route: {
						params: {
							id: 1
						}
					}
				},
			}
		});
		expect(mockRouter.push).toHaveBeenCalledWith("/");
		expect(mockToast.info).toHaveBeenCalled();
	});
});

