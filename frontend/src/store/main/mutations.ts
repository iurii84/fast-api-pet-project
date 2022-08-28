import {  ISensorAvailableList, ISensorNotRegisteredList, IUserProfile, ICompressResponse, ISensorRegisterResponse } from '@/interfaces';
import { MainState, AppNotification } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';


export const mutations = {
    setRegisterSensor(state: MainState, payload: ISensorRegisterResponse) {
        state.registerSensor = payload;
    },
    setNotRegisteredSensors(state: MainState, payload: ISensorNotRegisteredList[]) {
        state.notRegisteredSensors = payload;
    },
    setAvailableSensors(state: MainState, payload: ISensorAvailableList[]) {
        state.availableSensors = payload;
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

export const commitSetAvailableSensors = commit(mutations.setAvailableSensors);
export const commitCompressDb = commit(mutations.setCompressDb);
export const commitSetNotRegisteredSensors = commit(mutations.setNotRegisteredSensors);
export const commitRegisterSensor = commit(mutations.setRegisterSensor);
