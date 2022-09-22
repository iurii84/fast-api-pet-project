export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IDeviceAvailableList {
    id: number;
    uuid: string;
    name: string;
    type: number;
    location: number;
    first_occurrence: string;
    date_registered: string;
}

export interface ICompressDbPayload {
    uuid: string;
    for_items_with_compress_ratio: number;
    start_date_time: string;
    end_date_time: string;
}



export interface ICompressResponse {
    task_id: string
}


export interface ITaskGetResponse {
    task_state: string,
    task: {
        items_found: number;
        is_even: boolean;
        items_selected_to_compress: null;
        db_update: number;
        db_delete: number;
    },
    task_message: string
}

export interface IDeviceNotRegisteredList {
    uuid: string;
    type: number;
    first_occurrence: string;
}

export interface IDeviceRegisterPost {
    uuid: string;
    name: string;
    location: number;
}

export interface IDeviceRegisterResponse {
    name: string;
    type: number;
    location: number;
    date_registered: string;
    id: number;
    uuid: string;
    first_occurrence: string;
}

export interface IDeviceLocationResponse {
    id: number;
    name: string;
    description: string;
}

export interface IDeviceTypeResponse {
    id: number;
    name: string;
    description: string;
}

export interface IDeviceDeleteResponse {
    id: number;
}

export interface IDeviceUpdateResponse {
    name: string;
    type: number;
    location: number;
    date_registered: string;
    id: number;
    uuid: string;
    first_occurrence: string;
}

export interface IDeviceUpdate {
    name: string;
    location: number;
}