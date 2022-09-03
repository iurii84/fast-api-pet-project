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
    
    available_sensors: (state: MainState) => state.availableSensors,
    compress_db: (state: MainState) => state.compressDbResponse,
    not_registered_sensors: (state: MainState) => state.notRegisteredSensors,
    sensor_locations: (state: MainState) => state.sensorLocations,
    sensor_types: (state: MainState) => state.sensorTypes
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

export const readAvailableSensors = read(getters.available_sensors);
export const readCompressDb = read(getters.compress_db);
export const readNotRegisteredSensors = read(getters.not_registered_sensors);
export const readSensorLocations = read(getters.sensor_locations);
export const readSensorTypes = read(getters.sensor_types);