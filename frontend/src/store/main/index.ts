import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { MainState } from './state';

const defaultState: MainState = {
  isLoggedIn: null,
  token: '',
  logInError: false,
  userProfile: null,
  dashboardMiniDrawer: false,
  dashboardShowDrawer: true,
  notifications: [],
  
  availableDevices: [],
  compressDbResponse: null,
  notRegisteredDevices: [],
  registerDevice: null,
  deleteDevice: null,
  updateDevice: null,
  deviceLocations: [],
  deviceTypes: []
};

export const mainModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
