<template>
    <div>
        <v-card class="ma-5 pa-5 no_blink" id="table_unregistered">
            <v-card-title primary-title>
                <div class="headline primary--text">Unregistered Devices</div>
            </v-card-title>

            <b-modal size="lg" title-tag="h4" ref="delete-device-confirm" hide-footer title="You are about to delete following device from the database:">
                <div class="d-block text-center">
                    
                    <div class="device_to_delete_fields">
                        <b>
                            <label for="device_id_to_delete">ID: </label>
                        </b>
                        <span id="device_id_to_delete">
                            {{device_selected_to_delete.id}}
                        </span>
                    </div>
                    
                    <div class="device_to_delete_fields">
                        <b>
                            <label for="device_uuid_to_delete" >UUID: </label> 
                        </b>
                        <span id="device_uuid_to_delete">
                            {{device_selected_to_delete.uuid}}
                        </span>
                    </div>

                    <div class="device_to_delete_fields">
                        <b>
                            <label for="device_name_to_delete" >NAME: </label> 
                        </b>
                        <span id="device_name_to_delete">
                            {{device_selected_to_delete.name}}
                        </span>
                    </div>
                     
                </div>
                <hr>
                <div id="delete-decision-buttons-group">
                    <b-button class="mt-3 decision-button" variant="primary" block @click="abortDeletingDevice">Cancel</b-button>
                    <b-button class="mt-3 decision-button" variant="danger" block @click="deleteDeviceAfterConfirm">Delete</b-button>
                </div>
                
            </b-modal>
       
            <div>
                <b-table striped hover sort-icon-left
                    :items="table_items" 
                    :fields="table_fields" 
                    :sort-by.sync="nonRegSortBy"
                    :sort-desc.sync="nonRegSortDesc"
                    label-sort-asc=""
                    label-sort-desc=""
                    label-sort-clear=""
                    v-model="currentItems">

                    <template v-slot:cell(type)="data">
                        <span  v-b-tooltip.hover :title=returnTypeToolTip(data.value)>{{ data.value}}</span>
                    </template>

                    <template v-slot:cell(actions)="{ detailsShowing, item }" >
                        <!-- Use the built in method from the scoped data to toggle the row details -->
                        <b-btn @click="toggleDetails(item)">{{ detailsShowing ? 'Close' : 'Register device'}}</b-btn>
                    </template>
                   
                    <template v-slot:row-details="{ item }">
                        <b-card>
                        <label for="field_input_uuid" class="field_input">UUID: </label>
                        <b-form-input v-model="item.uuid"  disabled class="field_input" id="field_input_uuid"> 
                        {{device_uuid = item.uuid}}    
                        </b-form-input>

                        <br>
                        
                        <label for="field_input_device_name" class="field_input">Device name: </label>
                        <b-form-input v-model="device_name_input" placeholder="Device name" class="field_input  blink" id="field_input_device_name">
                        </b-form-input>

                        <b-form-group id="device_select_location" label="Select device location:" label-for="device_location_selector" class="field_input" >
                            <v-select 
                                id="device_location_selector"  
                                v-model="device_location_input" 
                                :items="device_locations_api" 
                                item-text=name
                                required 
                                placeholder="Select device location"  
                                return-object
                            >
                            </v-select>
                            <div v-if="device_location_input != null">
                                <br>
                                description:  {{device_location_input.description}}
                            </div>
                        </b-form-group>

                        <br>

                        <b-button variant="primary" v-on:click = "register_device" v-bind:disabled="register_button_inactive">Register</b-button>
                    
                        </b-card>
                    </template>
                </b-table>    
            </div>
        </v-card>
        <v-card class="ma-5 pa-5 no_blink" id="table_registered">
            <v-card-title primary-title>
                <div class="headline primary--text">Registered Devices</div>
            </v-card-title>
            <div>
                <b-table striped hover sort-icon-left
                    :items="table_items_registered" 
                    :fields="table_fields_registered" 
                    :sort-by.sync="regSortBy"
                    :sort-desc.sync="regSortDesc"
                    label-sort-asc=""
                    label-sort-desc=""
                    label-sort-clear=""
                    v-model="currentItems_registered">

                   <template v-slot:cell(type)="data">
                        <span  v-b-tooltip.hover :title=returnTypeToolTip(data.value)>{{ data.value}}</span>
                    </template>

                    <template v-slot:cell(location)="data">
                        <span  v-b-tooltip.hover :title=returnLocationTooltip(data.value)>{{ data.value}}</span>
                    </template> 

                    <template v-slot:cell(actions)="{ detailsShowing, item }">                        
                        <v-icon class="registered_icons" @click="toggleDetailsRegistered(item)">{{ detailsShowing ? 'close' : 'edit'}}</v-icon>
                        <v-icon class="registered_icons" @click="deleteDevice(item)">delete</v-icon>
                    </template>

                    <template v-slot:row-details="{ item }">
                        <b-card>
                            <label for="field_input_id" class="field_input">ID: </label>
                            <b-form-input v-model="item.id"  disabled class="field_input" id="field_input_id"> 
                                {{device_update_id = item.id}}    
                            </b-form-input>

                            <label for="field_input_uuid" class="field_input">UUID: </label>
                            <b-form-input v-model="item.uuid"  disabled class="field_input" id="field_input_uuid"> 
                            </b-form-input>

                            <b-form-group id="device_select_location" label="Select device location:" label-for="device_location_selector" class="field_input" >
                                <v-select 
                                    id="device_location_selector"  
                                    v-model="device_update_location_input" 
                                    :items="device_locations_api" 
                                    item-text=name
                                    required 
                                    placeholder="Select device location"       
                                    return-object
                                >
                                </v-select>
                                                             
                                <!-- <div v-if="device_location_input != null">
                                    <br>
                                    description:  {{device_update_location_input.description}}
                                </div> -->
                            </b-form-group>

                            <label for="field_input_name" class="field_input">Name: </label>
                            <b-form-input v-model="item.name"   class="field_input  blink" id="field_input_name"> 
                                {{device_update_name_input = item.name}}
                            </b-form-input>

                            <br>

                            <b-button variant="primary" v-on:click = "update_device" v-bind:disabled="update_button_inactive">Update</b-button>
                        </b-card>
                    </template>                
                </b-table>
            </div>
        </v-card>
    </div> 
</template>

<script>
    import { Store } from 'vuex';
    import Vue from 'vue';
    import api from "@/api"
    import { mapState } from 'vuex';
    import { 
        dispatchGetNotRegisteredDevices, 
        dispatchRegisterDevice, 
        dispatchUpdateDevice,
        dispatchDeleteDevice,
        dispatchDeviceLocations,
        dispatchDeviceTypes,
        dispatchGetAwailableDevices 
        } from '@/store/main/actions';
    import { 
        readNotRegisteredDevices, 
        readDeviceLocations,
        readDeviceTypes,
        readAvailableDevices,
        readDeviceUpdateResponse
        } from '@/store/main/getters';

   
    export default { 
 
    methods: {
        register_device: function(){  
            this.register_button_inactive = true
            let register_device_obj = {
                "uuid": this.device_uuid,
                "name": this.device_name_input,
                "location": this.device_location_input.location_id
            }
            // perform api call to register device
            dispatchRegisterDevice(this.$store, register_device_obj)
            
            console.log(register_device_obj)
        },

        update_device: function(){
            this.update_button_inactive = true;
            let update_device_obj = {
                "name": this.device_update_name_input,
                "location": this.device_update_location_input.location_id
            }
            dispatchUpdateDevice(this.$store, {"payload": update_device_obj, "device_id": this.device_update_id})
            console.log(update_device_obj)
        },

        //finds a specific item based on the provided ID and toggles details on that item
        toggleDetails(row) {
            console.log("toggleDetails: " + JSON.stringify(row))
            if(row._showDetails){
            this.$set(row, '_showDetails', false)
            }
            else{
                this.currentItems.forEach(item => {
                    this.$set(item, '_showDetails', false)
                })

                this.$nextTick(() => {
                    this.$set(row, '_showDetails', true)
                })
            }
        },
        toggleDetailsRegistered(row) {
            console.log("toggleDetailsRegistered: " + JSON.stringify(row))
            if(row._showDetails){
            this.$set(row, '_showDetails', false)
            }
            else{
                this.currentItems_registered.forEach(item => {
                    this.$set(item, '_showDetails', false)
                })

                this.$nextTick(() => {
                    this.$set(row, '_showDetails', true)
                })
            }
        },
        typeUpdate() {
            // iterate over the all devices
            console.log("typeUpdate()")
            try { 
                if (this.device_types[0].type_id != null && this.table_items_registered[0].type != null) {
                    console.log("typeUpdate() - after if...")
                    let unreg_devices_arr = JSON.parse(JSON.stringify(this.table_items));
                    console.log("unreg_devices_arr: " + JSON.stringify(unreg_devices_arr))
                    for (let [index, val] of this.table_items.entries()) {
                        unreg_devices_arr[index].type = this.getTypeAttrById(val.type)  
                    }
                    this.table_items = unreg_devices_arr

                    let registered_devices_arr = JSON.parse(JSON.stringify(this.table_items_registered));
                    for (let [index, val] of this.table_items_registered.entries()) {
                        registered_devices_arr[index].type = this.getTypeAttrById(val.type)  
                    }
                    this.table_items_registered = registered_devices_arr
                }
            
            }
            catch (err) {
            }
            
           
            
        },
       
        getTypeAttrById(id) {
            // iterate over the all device_types. When found - return name, else return id
            let type_by_id;
            for (let item of this.device_types) {
                if (item.type_id === id) {
                    type_by_id = item.name
                    break
               }
               else {
                    type_by_id = id
               }   
            }
            return type_by_id
        },

        locationUpdate() {
            try { 
                if (this.device_locations_api[0].location_id != null && this.table_items_registered[0].location) {
                    let registered_devices_arr = JSON.parse(JSON.stringify(this.table_items_registered));
                    for (let [index, val] of this.table_items_registered.entries()) {
                        registered_devices_arr[index].location = this.getLocationAttrById(val.location)  
                    }
                    this.table_items_registered = registered_devices_arr
                }
                
            }
            catch (err) {
            }   
        },

        getLocationAttrById(id) {
            // iterate over the all devices types. When found - return name, else return id
            let location_by_id;
            for (let item of this.device_locations_api) {
                if (item.location_id === id) {
                    location_by_id = item.name
                    break
               }
               else {
                    location_by_id = id
               }   
            }
            return location_by_id
        },

        returnTypeToolTip(item_name) {
            let type_descr_by_name;
            for (let item of this.device_types) {
                if (item.name === item_name) {
                    type_descr_by_name = item.description
                    break
               }
               else {
                    type_descr_by_name = item_name
               }   
            }
            return type_descr_by_name
        }, 
        returnLocationTooltip(item_name) {
            let loc_by_name;
            for (let item of this.device_locations_api) {
                if (item.name === item_name) {
                    loc_by_name = item.description
                    break
                }
                else {
                    loc_by_name = item_name
                }   
            }
            return loc_by_name;
        },
        
        deleteDevice(item) {
            this.device_selected_to_delete = item
            console.log("DEVICE SELECTED TO DELETE: " + JSON.stringify(item.id))
            this.$refs['delete-device-confirm'].show()
        },
        deleteDeviceAfterConfirm() {
            console.log("DELETE DEVICE AFTER CONFIRM: " + this.device_id_selected_to_delete)
            dispatchDeleteDevice(this.$store, this.device_selected_to_delete.id)
            this.device_selected_to_delete = {}
            this.$refs['delete-device-confirm'].hide()
            
        },
        abortDeletingDevice() {
            this.device_selected_to_delete = {}
            this.$refs['delete-device-confirm'].hide()
        }

    },

   computed: {
        //need to define computed and watch function with the same name to watch vuex changes
        readNotRegisteredDevices: function(){
            return readNotRegisteredDevices(this.$store)
        },
        readAvailableDevices: function(){
            return readAvailableDevices(this.$store)
        },
        readDeviceLocations: function(){
            return readDeviceLocations(this.$store)
        },
        readDeviceTypes: function(){
            return readDeviceTypes(this.$store)
        },
        readDeviceUpdateResponse: function(){
            return readDeviceUpdateResponse(this.$store)
        }
   },
   
   watch: {
        readNotRegisteredDevices(newValue, oldValue) {
            //on vuex parameter change - execute this function
            var not_registered_devices_arr = []
            newValue.forEach(element => {
                var list_obj = {uuid: element.uuid, first_occurrence: element.first_occurrence, type: element.type}
                not_registered_devices_arr.push(list_obj)
            });

            this.table_items = not_registered_devices_arr
            this.register_button_inactive = false
            this.typeUpdate()
        },
        readAvailableDevices(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.table_items_registered = newValue
            this.typeUpdate()
            this.locationUpdate()
        },
        readDeviceLocations(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.device_locations_api = newValue

            this.locationUpdate()
        },
        readDeviceTypes(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.device_types = newValue
            this.typeUpdate()
        },
        readDeviceUpdateResponse(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.update_button_inactive = false
        },
        
    },

    data() {
        return {
            register_button_inactive: false,
            update_button_inactive: false,

            device_uuid: '',
            device_name_input: '',
            device_location_input: null,

            device_update_id: '',
            device_update_name_input: '',
            device_update_location_input: null,
            
            device_locations_api: [],
            device_types: [],
            
            nonRegSortBy: 'first_occurrence',
            regSortBy: 'date_registered',
            nonRegSortDesc: false,
            regSortDesc: true,
          
            currentItems: [],
            currentItems_registered: [],
            table_fields: [
                {key: "uuid", sortable: true}, 
                {key: "first_occurrence", sortable: true}, 
                {key: "type", sortable: true},
                {key: 'actions', label: 'Actions'},
            ],
            table_items: [],
            table_fields_registered: [
                {key: "name", sortable: true}, 
                {key: "location", sortable: true},
                {key: "type", sortable: true},
                {key: "date_registered", sortable: true}, 
                {key: 'actions', label: 'Actions'},
            ],
            table_items_registered: [],
            not_registered_devices: false,

            device_selected_to_delete: {}
           
        }
    },
  
    mounted() {
        // called for initiate the list of devices load from api 
        dispatchGetNotRegisteredDevices(this.$store)
        dispatchDeviceLocations(this.$store)
        dispatchDeviceTypes(this.$store)
        dispatchGetAwailableDevices(this.$store)
    },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.field_input {
    margin: 3px; 
    width: 50%;   
}

.no_blink {
    caret-color: transparent;
}
.blink {
    caret-color: black;
}
.registered_icons {
    margin-right: 30px
}


.device_to_delete_fields {
    text-align: left;
}

#delete-decision-buttons-group {
    text-align: right;
}

.decision-button {
    margin-right: 10px;
}

</style>