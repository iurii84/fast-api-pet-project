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

export interface ISensorAvailableList {
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
    items_found: number;
    is_even: boolean;
    items_selected_to_compress: null;
    db_update: number;
    db_delete: number;
  }