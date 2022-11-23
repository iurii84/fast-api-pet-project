import {
    IDeviceAvailableList,
    IDeviceNotRegisteredList,
    IUserProfile,
    ICompressResponse,
    IDeviceRegisterResponse,
    IDeviceLocationResponse,
    IDeviceTypeResponse,
    IDeviceDeleteResponse,
    IDeviceUpdateResponse,
    IDeviceDataBindList,
    IDeviceGetParams,
    IDataBingRegisterResponse,
    IDatabindDeleteResponse,
    IDatabindUpdateResponse,
    IPostStaticDisplayFrame,
    IGetStaticDisplayFrame,
} from '@/interfaces';
import { MainState, AppNotification } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';


export const mutations = {
    setStaticDisplayDataList(state: MainState, payload: IGetStaticDisplayFrame[]) {
        state.getStaticDisplayFrameList = payload;
    },
    setRegisterStaticDisplayFrame(state: MainState, payload: IPostStaticDisplayFrame) {
        state.registerStaticDisplayFrame = payload;
    },
    setSubscribedDataBindList(state: MainState, payload: IDeviceDataBindList[]) {
        state.subscribedDataBind = payload;
    },
    setUpdateDatabind(state: MainState, payload: IDatabindUpdateResponse) {
        state.updateDatabind = payload;
    },
    setDeleteDatabind(state: MainState, payload: IDatabindDeleteResponse) {
        state.deleteDevice = payload;
    },
    setRegisterDataBind(state: MainState, payload: IDataBingRegisterResponse) {
        state.registerDataBind = payload;
    },
    setDeviceGetParams(state: MainState, payload: IDeviceGetParams) {
        state.deviceGetParams = payload;
    },
    setDeviceDataBindList(state: MainState, payload: IDeviceDataBindList[]) {
        state.deviceDataBind = payload;
    },
    setDeviceTypes(state: MainState, payload: IDeviceTypeResponse[]) {
        state.deviceTypes = payload;
    },
    setDeviceLocations(state: MainState, payload: IDeviceLocationResponse[]) {
        state.deviceLocations = payload;
    },
    setRegisterDevice(state: MainState, payload: IDeviceRegisterResponse) {
        state.registerDevice = payload;
    },
    setDeleteDevice(state: MainState, payload: IDeviceDeleteResponse) {
        state.deleteDevice = payload;
    },
    setUpdateDevice(state: MainState, payload: IDeviceUpdateResponse) {
        state.updateDevice = payload;
    },
    setNotRegisteredDevices(state: MainState, payload: IDeviceNotRegisteredList[]) {
        state.notRegisteredDevices = payload;
    },
    setAvailableDevices(state: MainState, payload: IDeviceAvailableList[]) {
        state.availableDevices = payload;
    },
    setAvailableDisplayDevices(state: MainState, payload: IDeviceAvailableList[]) {
        state.availableDisplayDevices = payload;
    },
    setCompressDb(state: MainState, payload: ICompressResponse) {
        state.compressDbResponse = payload;
    },
    setToken(state: MainState, payload: string) {
        state.token = payload;
    },
    setLoggedIn(state: MainState, payload: boolean) {
        state.isLoggedIn = payload;
    },
    setLogInError(state: MainState, payload: boolean) {
        state.logInError = payload;
    },
    setUserProfile(state: MainState, payload: IUserProfile) {
        state.userProfile = payload;
    },
    setDashboardMiniDrawer(state: MainState, payload: boolean) {
        state.dashboardMiniDrawer = payload;
    },
    setDashboardShowDrawer(state: MainState, payload: boolean) {
        state.dashboardShowDrawer = payload;
    },
    addNotification(state: MainState, payload: AppNotification) {
        state.notifications.push(payload);
    },
    removeNotification(state: MainState, payload: AppNotification) {
        state.notifications = state.notifications.filter((notification) => notification !== payload);
    },
};

const {commit} = getStoreAccessors<MainState | any, State>('');

export const commitSetDashboardMiniDrawer = commit(mutations.setDashboardMiniDrawer);
export const commitSetDashboardShowDrawer = commit(mutations.setDashboardShowDrawer);
export const commitSetLoggedIn = commit(mutations.setLoggedIn);
export const commitSetLogInError = commit(mutations.setLogInError);
export const commitSetToken = commit(mutations.setToken);
export const commitSetUserProfile = commit(mutations.setUserProfile);
export const commitAddNotification = commit(mutations.addNotification);
export const commitRemoveNotification = commit(mutations.removeNotification);

export const commitSetAvailableDevices = commit(mutations.setAvailableDevices);
export const commitCompressDb = commit(mutations.setCompressDb);
export const commitSetNotRegisteredDevices = commit(mutations.setNotRegisteredDevices);
export const commitRegisterDevice = commit(mutations.setRegisterDevice);
export const commitRegisterDisplayDevice = commit(mutations.setAvailableDisplayDevices);
export const commitDeleteDevice = commit(mutations.setDeleteDevice);
export const commitUpdateDevice = commit(mutations.setUpdateDevice);
export const commitSetDeviceLocations = commit(mutations.setDeviceLocations);
export const commitSetDeviceTypes = commit(mutations.setDeviceTypes);
export const commitDeviceDataBindList = commit(mutations.setDeviceDataBindList);
export const commitDeviceGetParams = commit(mutations.setDeviceGetParams);
export const commitRegisterDataBind = commit(mutations.setRegisterDataBind);
export const commitDeleteDatabind = commit(mutations.setDeleteDatabind);
export const commitUpdateDatabind = commit(mutations.setUpdateDatabind);
export const commitSubscribedDataBindList = commit(mutations.setSubscribedDataBindList);
export const commitRegisterStaticDisplayFrame = commit(mutations.setRegisterStaticDisplayFrame);
export const commitGetStaticDisplayDataList = commit(mutations.setStaticDisplayDataList);