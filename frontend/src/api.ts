import axios from 'axios';
import { apiUrl } from '@/env';
import {
  IDeviceAvailableList,
  IDeviceNotRegisteredList,
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  ICompressDbPayload,
  ICompressResponse,
  IDeviceRegisterResponse,
  IDeviceRegisterPost,
  IDeviceLocationResponse,
  IDeviceTypeResponse,
  IDeviceUpdate,
  ITaskGetResponse,
  IDeviceDataBindList,
  IDeviceGetParams,
  IDataBingRegisterPost,
  IDataBingRegisterResponse,
  IDatabindUpdatePatch,
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async updateDatabind(token: string, data: IDatabindUpdatePatch, deviceId: number) {
    return axios.patch(`${apiUrl}/api/v1/device_data_bind/${deviceId}`, data);
  },
  async deleteDatabind(token: string, deviceId: number) {
    return axios.delete(`${apiUrl}/api/v1/device_data_bind/${deviceId}`);
  },
  async registerDataBind(token: string, data: IDataBingRegisterPost) {
    return axios.post<IDataBingRegisterResponse>(`${apiUrl}/api/v1/device_data_bind`, data);
  },
  async getDeviceParams(device_uuid: string) {
    return axios.get<IDeviceGetParams>(`${apiUrl}/api/v1/device/get_params_by_uuid/${device_uuid}`);
  },
  async getDeviceDataBindList() {
    return axios.get<IDeviceDataBindList[]>(`${apiUrl}/api/v1/device_data_bind`);
  },
  async updateDevice(token: string, data: IDeviceUpdate, deviceId: number) {
    return axios.patch(`${apiUrl}/api/v1/device/${deviceId}`, data);
  },
  async deleteDevice(token: string, deviceId: number) {
    return axios.delete(`${apiUrl}/api/v1/device/${deviceId}`);
  },
  async getDeviceTypes() {
    return axios.get<IDeviceTypeResponse[]>(`${apiUrl}/api/v1/device_type`);
  },
  async getDeviceLocations() {
    return axios.get<IDeviceLocationResponse[]>(`${apiUrl}/api/v1/device_location`);
  },
  async registerDevice(token: string, data: IDeviceRegisterPost) {
    return axios.post<IDeviceRegisterResponse>(`${apiUrl}/api/v1/device/register`, data);
  },
  async getDevices(is_display: boolean = false) {
    return axios.get<IDeviceAvailableList[]>(`${apiUrl}/api/v1/device`, { params: { is_display } });
  },
  async getNotRegisteredDevices() {
    return axios.get<IDeviceNotRegisteredList[]>(`${apiUrl}/api/v1/device/get_unregistered`);
  },
  async getTask(token: string, task_id: string) {
    return axios.get<ITaskGetResponse>(`${apiUrl}/api/v1/task/`, { params: { task_id } });
  },
  async compressDb(token: string, data: ICompressDbPayload) {
    return axios.post<ICompressResponse>(`${apiUrl}/api/v1/message/compress`, data);
  },

  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
};
