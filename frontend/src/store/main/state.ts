import { ISensorAvailableList, IUserProfile, ICompressResponse} from '@/interfaces';

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
    
    availableSensors: ISensorAvailableList[];
    compressDbResponse: ICompressResponse | null
}
