import { api } from '@/api';
import { IDeviceUpdate } from '@/interfaces';
import router from '@/router';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { AxiosError } from 'axios';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import {
    commitAddNotification,
    commitRemoveNotification,
    commitSetAvailableDevices,
    commitSetLoggedIn,
    commitSetLogInError,
    commitSetToken,
    commitSetUserProfile,
    commitCompressDb,
    commitSetNotRegisteredDevices,
    commitRegisterDevice,
    commitSetDeviceLocations,
    commitSetDeviceTypes,
    commitDeleteDevice,
    commitUpdateDevice,
} from './mutations';
import { AppNotification, MainState } from './state';

type MainContext = ActionContext<MainState, State>;

export const actions = {
    async actionLogIn(context: MainContext, payload: { username: string; password: string }) {
        try {
            const response = await api.logInGetToken(payload.username, payload.password);
            const token = response.data.access_token;
            if (token) {
                saveLocalToken(token);
                commitSetToken(context, token);
                commitSetLoggedIn(context, true);
                commitSetLogInError(context, false);
                await dispatchGetUserProfile(context);
                await dispatchRouteLoggedIn(context);
                commitAddNotification(context, { content: 'Logged in', color: 'success' });
            } else {
                await dispatchLogOut(context);
            }
        } catch (err) {
            commitSetLogInError(context, true);
            await dispatchLogOut(context);
        }
    },
    async actionGetUserProfile(context: MainContext) {
        try {
            const response = await api.getMe(context.state.token);
            if (response.data) {
                commitSetUserProfile(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateUserProfile(context: MainContext, payload) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateMe(context.state.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetUserProfile(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Profile successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCheckLoggedIn(context: MainContext) {
        if (!context.state.isLoggedIn) {
            let token = context.state.token;
            if (!token) {
                const localToken = getLocalToken();
                if (localToken) {
                    commitSetToken(context, localToken);
                    token = localToken;
                }
            }
            if (token) {
                try {
                    const response = await api.getMe(token);
                    commitSetLoggedIn(context, true);
                    commitSetUserProfile(context, response.data);
                } catch (error) {
                    await dispatchRemoveLogIn(context);
                }
            } else {
                await dispatchRemoveLogIn(context);
            }
        }
    },
    async actionRemoveLogIn(context: MainContext) {
        removeLocalToken();
        commitSetToken(context, '');
        commitSetLoggedIn(context, false);
    },
    async actionLogOut(context: MainContext) {
        await dispatchRemoveLogIn(context);
        await dispatchRouteLogOut(context);
    },
    async actionUserLogOut(context: MainContext) {
        await dispatchLogOut(context);
        commitAddNotification(context, { content: 'Logged out', color: 'success' });
    },
    actionRouteLogOut(context: MainContext) {
        if (router.currentRoute.path !== '/login') {
            router.push('/login');
        }
    },
    async actionCheckApiError(context: MainContext, payload: AxiosError) {
        if (payload.response!.status === 401) {
            await dispatchLogOut(context);
        }
    },
    actionRouteLoggedIn(context: MainContext) {
        if (router.currentRoute.path === '/login' || router.currentRoute.path === '/') {
            router.push('/main');
        }
    },
    async removeNotification(context: MainContext, payload: { notification: AppNotification, timeout: number }) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                commitRemoveNotification(context, payload.notification);
                resolve(true);
            }, payload.timeout);
        });
    },
    async passwordRecovery(context: MainContext, payload: { username: string }) {
        const loadingNotification = { content: 'Sending password recovery email', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.passwordRecovery(payload.username),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Password recovery email sent', color: 'success' });
            await dispatchLogOut(context);
        } catch (error) {
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { color: 'error', content: 'Incorrect username' });
        }
    },
    async resetPassword(context: MainContext, payload: { password: string, token: string }) {
        const loadingNotification = { content: 'Resetting password', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.resetPassword(payload.password, payload.token),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Password successfully reset', color: 'success' });
            await dispatchLogOut(context);
        } catch (error) {
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { color: 'error', content: 'Error resetting password' });
        }
    },
    async actionGetDevices(context: MainContext) {
        try {
            const response = await api.getDevices();
            if (response.data) {
                commitSetAvailableDevices(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }

    },

    async actionCompressDb(context: MainContext, payload) {
        try {
            const loadingNotification = { content: 'compressing DB...', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.compressDb(context.state.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 3600)),
            ]))[0];
            commitCompressDb(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'DB successfully compressed', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },

    async actionGetNotRegisteredDevices(context: MainContext) {
        try {
            const response = await api.getNotRegisteredDevices();
            if (response.data) {
                commitSetNotRegisteredDevices(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }

    },

    async actionRegisterDevice(context: MainContext, payload) {
        try {
            const response = (await Promise.all([
                api.registerDevice(context.state.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRegisterDevice(context, response.data);
            commitAddNotification(context, { content: 'Device ' + response.data.uuid + ' successfully registered!', color: 'success' });
            // update list of unregistered devices
            dispatchGetNotRegisteredDevices(context)
            // update list of registered devices
            dispatchGetAwailableDevices(context)
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },

    async actionUpdateDevice(context: MainContext, data) {
        try {
            const response = (await Promise.all([
                api.updateDevice(context.state.token, data.payload, data.device_id),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitUpdateDevice(context, response.data);
            commitAddNotification(context, { content: 'Device ' + response.data.uuid + ' successfully updated!', color: 'success' });
            
            // update list of registered devices
            dispatchGetAwailableDevices(context)
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },

    async actionDeleteDevice(context: MainContext, device_id: number) {
        try {
            const response = (await Promise.all([
                api.deleteDevice(context.state.token, device_id),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitDeleteDevice(context, response.data);
            commitAddNotification(context, { content: 'Device with id ' + response.data.id + ' was successfully removed from DB!', color: 'success' });
            // update list of unregistered devices
            dispatchGetNotRegisteredDevices(context)
            // update list of registered devices
            dispatchGetAwailableDevices(context)
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },

    async actionGetDeviceLocations(context: MainContext) {
        try {
            const response = await api.getDeviceLocations();
            if (response.data) {
                commitSetDeviceLocations(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }

    },

    async actionGetDeviceTypes(context: MainContext) {
        try {
            const response = await api.getDeviceTypes();
            if (response.data) {
                commitSetDeviceTypes(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }

    },
};

const { dispatch } = getStoreAccessors<MainState | any, State>('');

export const dispatchCheckApiError = dispatch(actions.actionCheckApiError);
export const dispatchCheckLoggedIn = dispatch(actions.actionCheckLoggedIn);
export const dispatchGetUserProfile = dispatch(actions.actionGetUserProfile);
export const dispatchLogIn = dispatch(actions.actionLogIn);
export const dispatchLogOut = dispatch(actions.actionLogOut);
export const dispatchUserLogOut = dispatch(actions.actionUserLogOut);
export const dispatchRemoveLogIn = dispatch(actions.actionRemoveLogIn);
export const dispatchRouteLoggedIn = dispatch(actions.actionRouteLoggedIn);
export const dispatchRouteLogOut = dispatch(actions.actionRouteLogOut);
export const dispatchUpdateUserProfile = dispatch(actions.actionUpdateUserProfile);
export const dispatchRemoveNotification = dispatch(actions.removeNotification);
export const dispatchPasswordRecovery = dispatch(actions.passwordRecovery);
export const dispatchResetPassword = dispatch(actions.resetPassword);

export const dispatchGetAwailableDevices = dispatch(actions.actionGetDevices);
export const dispatchedCompressDb = dispatch(actions.actionCompressDb);
export const dispatchGetNotRegisteredDevices = dispatch(actions.actionGetNotRegisteredDevices);
export const dispatchRegisterDevice = dispatch(actions.actionRegisterDevice);
export const dispatchDeleteDevice = dispatch(actions.actionDeleteDevice);
export const dispatchUpdateDevice = dispatch(actions.actionUpdateDevice);
export const dispatchDeviceLocations = dispatch(actions.actionGetDeviceLocations);
export const dispatchDeviceTypes = dispatch(actions.actionGetDeviceTypes);