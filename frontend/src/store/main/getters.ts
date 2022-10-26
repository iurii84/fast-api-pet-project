import { MainState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    hasAdminAccess: (state: MainState) => {
        return (
            state.userProfile &&
            state.userProfile.is_superuser && state.userProfile.is_active);
    },
    loginError: (state: MainState) => state.logInError,
    dashboardShowDrawer: (state: MainState) => state.dashboardShowDrawer,
    dashboardMiniDrawer: (state: MainState) => state.dashboardMiniDrawer,
    userProfile: (state: MainState) => state.userProfile,
    token: (state: MainState) => state.token,
    isLoggedIn: (state: MainState) => state.isLoggedIn,
    firstNotification: (state: MainState) => state.notifications.length > 0 && state.notifications[0],

    available_devices: (state: MainState) => state.availableDevices,
    available_display_devices: (state: MainState) => state.availableDisplayDevices,
    compress_db: (state: MainState) => state.compressDbResponse,
    not_registered_devices: (state: MainState) => state.notRegisteredDevices,
    device_locations: (state: MainState) => state.deviceLocations,
    device_types: (state: MainState) => state.deviceTypes,
    device_update_response: (state: MainState) => state.updateDevice,
    device_data_bind_list: (state: MainState) => state.deviceDataBind,
    device_params: (state: MainState) => state.deviceGetParams,
    register_databind_response: (state: MainState) => state.registerDataBind,
    update_databind_response: (state: MainState) => state.updateDatabind,
};

const {read} = getStoreAccessors<MainState, State>('');

export const readDashboardMiniDrawer = read(getters.dashboardMiniDrawer);
export const readDashboardShowDrawer = read(getters.dashboardShowDrawer);
export const readHasAdminAccess = read(getters.hasAdminAccess);
export const readIsLoggedIn = read(getters.isLoggedIn);
export const readLoginError = read(getters.loginError);
export const readToken = read(getters.token);
export const readUserProfile = read(getters.userProfile);
export const readFirstNotification = read(getters.firstNotification);

export const readAvailableDevices = read(getters.available_devices);
export const readAvailableDisplayDevices = read(getters.available_display_devices);
export const readCompressDb = read(getters.compress_db);
export const readNotRegisteredDevices = read(getters.not_registered_devices);
export const readDeviceLocations = read(getters.device_locations);
export const readDeviceTypes = read(getters.device_types);
export const readDeviceUpdateResponse = read(getters.device_update_response);
export const readDeviceDataBindList = read(getters.device_data_bind_list);
export const readDeviceParams = read(getters.device_params);
export const readRegisterDataBindResponse = read(getters.register_databind_response);
export const readUpdateDatabindResponse = read(getters.update_databind_response);
