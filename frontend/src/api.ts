import axios from 'axios';
import { apiUrl } from '@/env';
import {
  ISensorAvailableList, 
  ISensorNotRegisteredList, 
  IUserProfile, 
  IUserProfileUpdate, 
  IUserProfileCreate, 
  ICompressDbPayload, 
  ICompressResponse, 
  ISensorRegisterResponse, 
  ISensorRegisterPost
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async registerSensor(token: string, data: ISensorRegisterPost) { 
    return axios.post<ISensorRegisterResponse>(`${apiUrl}/api/v1/sensor/register`, data);
  },
  async getSensors() { 
    return axios.get<ISensorAvailableList[]>(`${apiUrl}/api/v1/sensor`);
  },
  async getNotRegisteredSensors() { 
    return axios.get<ISensorNotRegisteredList[]>(`${apiUrl}/api/v1/sensor/get_unregistered`);
  },
  async compressDb(token: string, data: ICompressDbPayload) {
    return axios.post<ICompressResponse>(`${apiUrl}/api/v1/message/compress_after_date_time`, data);
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
