import {
    IDeviceAvailableList,
    IUserProfile,
    ICompressResponse,
    IDeviceNotRegisteredList,
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
} from '@/interfaces';

export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
}

export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: boolean;
    userProfile: IUserProfile | null;
    dashboardMiniDrawer: boolean;
    dashboardShowDrawer: boolean;
    notifications: AppNotification[];

    availableDevices: IDeviceAvailableList[];
    availableDisplayDevices: IDeviceAvailableList[];
    compressDbResponse: ICompressResponse | null;
    notRegisteredDevices: IDeviceNotRegisteredList[];
    registerDevice: IDeviceRegisterResponse | null;
    deleteDevice: IDeviceDeleteResponse | null;
    updateDevice: IDeviceUpdateResponse | null;
    deviceLocations: IDeviceLocationResponse[];
    deviceTypes: IDeviceTypeResponse[];
    deviceDataBind: IDeviceDataBindList[];
    deviceGetParams: IDeviceGetParams | null;
    registerDataBind: IDataBingRegisterResponse | null;
    deleteDatabind: IDatabindDeleteResponse | null;
    updateDatabind: IDatabindUpdateResponse | null;
    subscribedDataBind: IDeviceDataBindList[];
}
