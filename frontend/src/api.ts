const axios = require('axios').default;
import { apiUrl } from '@/env';
import {
  
  IUserProfileUpdate,
  IUserProfileCreate,
  ICompressDbPayload,
  IDeviceRegisterPost,
  IDeviceUpdate,
  IDataBingRegisterPost,
  IDatabindUpdatePatch,
  IPostStaticDisplayFrame,
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async getStaticDisplayFrames() {
    let response = await axios.get(`${apiUrl}/api/v1/static_display_data`);
    return response
  },
  async postStaticDisplayFrame(token: string, data: IPostStaticDisplayFrame) {
    let response = await axios.post(`${apiUrl}/api/v1/static_display_data`, data);
    return response
  },
  async getSubscribedDataBindList(subscriber_uuid: string) {
    let response = await axios.get(`${apiUrl}/api/v1/device_data_bind`, { params: { subscriber_uuid } });
    return response
  },
  async updateDatabind(token: string, data: IDatabindUpdatePatch, deviceId: number) {
    return await axios.patch(`${apiUrl}/api/v1/device_data_bind/${deviceId}`, data);
  },
  async deleteDatabind(token: string, deviceId: number) {
    return await axios.delete(`${apiUrl}/api/v1/device_data_bind/${deviceId}`);
  },
  async registerDataBind(token: string, data: IDataBingRegisterPost) {
    let response = await axios.post(`${apiUrl}/api/v1/device_data_bind`, data);
    return response
  },
  async getDeviceParams(device_uuid: string) {
    let response = await axios.get(`${apiUrl}/api/v1/device/get_params_by_uuid/${device_uuid}`);
    return response
  },
  async getDeviceDataBindList() {
    let response = await axios.get(`${apiUrl}/api/v1/device_data_bind`);
    return response
  },
  async updateDevice(token: string, data: IDeviceUpdate, deviceId: number) {
    return await axios.patch(`${apiUrl}/api/v1/device/${deviceId}`, data);
  },
  async deleteDevice(token: string, deviceId: number) {
    return await axios.delete(`${apiUrl}/api/v1/device/${deviceId}`);
  },
  async getDeviceTypes() {
    let response = await axios.get(`${apiUrl}/api/v1/device_type`);
    return response
  },
  async getDeviceLocations() {
    let response = await axios.get(`${apiUrl}/api/v1/device_location`);
    return response
  },
  async registerDevice(token: string, data: IDeviceRegisterPost) {
    let response = await axios.post(`${apiUrl}/api/v1/device/register`, data);
    return response
  },
  async getDevices(is_display: boolean = false) {
    let response = await axios.get(`${apiUrl}/api/v1/device`, { params: { is_display } });
    return response
  },
  async getNotRegisteredDevices() {
    let response = await axios.get(`${apiUrl}/api/v1/device/get_unregistered`);
    return response
  },
  async getTask(token: string, task_id: string) {
    let response = await axios.get(`${apiUrl}/api/v1/task/`, { params: { task_id } });
    return response
  },
  async compressDb(token: string, data: ICompressDbPayload) {
    let response = await axios.post(`${apiUrl}/api/v1/message/compress`, data);
    return response
  },

  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return await axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    let response = await axios.get(`${apiUrl}/api/v1/users/me`, authHeaders(token));
    return response
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    let response = await axios.put(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
    return response
  },
  async getUsers(token: string) {
    let response = await axios.get(`${apiUrl}/api/v1/users/`, authHeaders(token));
    return response
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return await axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return await axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return await axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return await axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
};
