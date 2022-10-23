<template>
    <v-card class="ma-5 pa-5">
        <v-card-title primary-title>
            <div class="headline primary--text">Device Data Bind</div>
        </v-card-title>

        <!-- Delete detabind modal -->
        <b-modal size="lg" title-tag="h4" ref="delete-databind-confirm" hide-footer title="You are about to delete following databind from the database:">
            <div v-if="databind_selected_to_delete != null" class="d-block text-center">
                <div  class="databind_to_delete_fields">
                    <b>
                        <label for="databind_id_to_delete">ID: </label>
                    </b>
                    <span id="databind_id_to_delete">
                        {{databind_selected_to_delete.id}}
                    </span>
                </div>

                <div  class="databind_to_delete_fields">
                    <b>
                        <label for="databind_name_to_delete">NAME: </label>
                    </b>
                    <span id="databind_name_to_delete">
                        {{databind_selected_to_delete.binder_name}}
                    </span>
                </div>
                    
            </div>
            <hr>
            <div id="delete-decision-buttons-group">
                <b-button class="mt-3 databind_btn" variant="primary" @click="abortDeletingDatabind">Cancel</b-button>
                <b-button class="mt-3 databind_btn" variant="danger"  @click="deleteDatabindAfterConfirm">Delete databind</b-button>
            </div>
            
        </b-modal>

        <!-- Create databind modal -->
        <b-button v-b-modal.modal_create_data_bind id="create_data_bind_btn">Create data bind</b-button>

        <div>
            <b-modal 
                id="modal_create_data_bind" 
                title="Create data bind:" 
                size="lg"
                hide-footer
                ref="create_databind_modal">
            
                <b-form @submit.stop.prevent="registerDataBind" @reset="registerDataBindReset">
                    <b-form-group id="databind_name_group" label="Databind name:" label-for="databind_name_input" class="field_input" >
                        <b-form-input
                            id="databind_name_input"
                            v-model="databind_name_input"
                            type="text"

                            v-validate="{ required: true, min: 5, max: 30 }"
                            name="databind_name_input"
                            :state="validateState('databind_name_input')"
                            aria-describedby="databind_name-feedback"
                            data-vv-as="Databind name"
                            > 
                        </b-form-input>
                        <b-form-invalid-feedback id="databind_name-feedback">
                            {{veeErrors.first("databind_name_input")}}
                        </b-form-invalid-feedback>
                    </b-form-group>

                    <b-form-group id="device_selector_group" label="Select device:" label-for="device_selector" class="field_input" >
                        <b-form-select 
                            class="no_blink"       
                            id="device_selector"  
                            v-model="selected_device" 
                            text-field="name"
                            @change="onDeviceSelected"
                            
                            v-validate="{ required: true }"
                            name="databind_device_input"
                            :state="validateState('databind_device_input')"
                            aria-describedby="databind_device-feedback"
                            data-vv-as="Databind device">

                            <option :value="null" disabled>-- Select device --</option>
                            <option v-for="option in registered_devices" :value="option">
                                {{ option.name }}
                            </option>
                        </b-form-select> 
                        <b-form-invalid-feedback id="databind_device-feedback">
                            {{veeErrors.first("databind_device_input")}}
                        </b-form-invalid-feedback>

                        
                    </b-form-group>

                    <b-form-group id="device_param_selector_group" label="Select device parameter:" label-for="device_parameter_selector" class="field_input" >
                        <b-form-select 
                            class="no_blink"       
                            id="device_parameter_selector"  
                            v-model="selected_param"
                            :options="device_params" 
                            
                            v-validate="{ required: true }"
                            name="databind_param_input"
                            :state="validateState('databind_param_input')"
                            aria-describedby="databind_param-feedback"
                            data-vv-as="Databind parameter"
                        >
                        <option :value="null" disabled>-- Select device parameter --</option>
                        </b-form-select>
                        <b-form-invalid-feedback id="databind_param-feedback">
                            {{veeErrors.first("databind_param_input")}}
                        </b-form-invalid-feedback>
                    </b-form-group>

                    <b-form-group id="subscriber_device_selector_group" label="Select subscriber device:" label-for="subscriber_device_selector" class="field_input" >
                        <b-form-select 
                            class="no_blink"       
                            id="subscriber_device_selector"  
                            v-model="selected_subscriber"

                            v-validate="{ required: true }"
                            name="databind_subscriber_input"
                            :state="validateState('databind_subscriber_input')"
                            aria-describedby="databind_subscriber-feedback"
                            data-vv-as="Databind subscriber"
                        >
                        <option :value="null" disabled>-- Select subscriber --</option>
                        <option v-for="option in display_devices_list" :value="option">
                            {{ option.name }}
                        </option>
                        </b-form-select>
                        <b-form-invalid-feedback id="databind_subscriber-feedback">
                            {{veeErrors.first("databind_subscriber_input")}}
                        </b-form-invalid-feedback>
                    </b-form-group>

                    <b-form-group id="databind_placeholder_data_group" label="Databind placeholder size:" label-for="databind_placeholder_data_selector" class="field_input" >
                        <b-form-input
                            id="databind_placeholder_data_selector"
                            v-model="placeholder_lenght"
                            min=1
                            type="number"> 
                        </b-form-input>
                    </b-form-group>

                    <hr>

                    <div>
                        <b-button class="databind_btn" type="submit" variant="primary">Create databind</b-button>
                        <b-button class="databind_btn"  type="reset">Reset</b-button>
                    </div>
                    
                </b-form>
            </b-modal>
        </div>

        <!-- Databind table -->
        <div class="no_blink">
            <b-table striped hover sort-icon-left
                id="databind_table"
                :items="table_items" 
                :fields="table_fields" 
                :sort-by.sync="nonRegSortBy"
                :sort-desc.sync="nonRegSortDesc"
                label-sort-asc=""
                label-sort-desc=""
                label-sort-clear=""
                v-model="currentItem"> 
            
                <template v-slot:cell(actions)="{ detailsShowing, item }">                        
                    <v-icon class="registered_icons" @click="toggleDetailsRegistered(item)">{{ detailsShowing ? 'close' : 'edit'}}</v-icon>
                    <v-icon class="registered_icons" @click="deleteDatabind(item)">delete</v-icon>
                </template>

                <template v-slot:row-details="{ item }">
                    
                    <b-card>
                        <b-form @submit.stop.prevent="updateDatabind(item)">

                            <b-form-group id="databind_name_group" label="Databind name:" label-for="databind_name_input" class="field_input" >
                                <b-form-input
                                    id="databind_name_input"
                                    v-model="databind_name_input"
                                    type="text"
                                    v-validate="{ required: true, min: 5, max: 30}"
                                    name="databind_name_input"
                                    :state="validateState('databind_name_input')"
                                    aria-describedby="databind_name-feedback"
                                    data-vv-as="Databind name"
                                    > 
                                </b-form-input>
                                <b-form-invalid-feedback id="databind_name-feedback">
                                    {{veeErrors.first("databind_name_input")}}
                                </b-form-invalid-feedback>
                            </b-form-group>

                            <b-form-group id="device_selector_group" label="Select device:" label-for="device_selector" class="field_input" >
                                <b-form-select 
                                    class="no_blink"       
                                    id="device_selector"  
                                    v-model="selected_device" 
                                    text-field="name"
                                    @change="onDeviceSelected"
                                    
                                    v-validate="{ required: true }"
                                    name="databind_device_input"
                                    :state="validateState('databind_device_input')"
                                    aria-describedby="databind_device-feedback"
                                    data-vv-as="Databind device">

                                    <option :value="null" disabled>-- Select device --</option>
                                    <option v-for="option in registered_devices" :value="option">
                                        {{ option.name }}
                                    </option>
                                </b-form-select> 
                                <b-form-invalid-feedback id="databind_device-feedback">
                                    {{veeErrors.first("databind_device_input")}}
                                </b-form-invalid-feedback>
                            </b-form-group>

                            <b-form-group id="device_param_selector_group" label="Select device parameter:" label-for="device_parameter_selector" class="field_input" >
                                <b-form-select 
                                    class="no_blink"       
                                    id="device_parameter_selector"  
                                    v-model="selected_param"
                                    :options="device_params"  
                                >
                                </b-form-select>
                            </b-form-group>

                            <b-form-group id="subscriber_device_selector_group" label="Select subscriber device:" label-for="subscriber_device_selector" class="field_input" >
                                <b-form-select 
                                    class="no_blink"       
                                    id="subscriber_device_selector"  
                                    v-model="selected_subscriber"
                                >
                                <option v-for="option in display_devices_list" :value="option">
                                    {{ option.name }}
                                </option>

                                </b-form-select>
                            </b-form-group>
                            
                            <b-form-group id="databind_placeholder_data_group" label="Databind placeholder size:" label-for="databind_placeholder_data_selector" class="field_input" >
                                <b-form-input
                                    id="databind_placeholder_data_selector"
                                    v-model="placeholder_lenght"
                                    min=1
                                    type="number"> 
                                </b-form-input>
                            </b-form-group>

                            <b-button type="submit" v-bind:disabled="update_button_inactive" variant="primary">Submit</b-button>
                        
                        </b-form>
                    </b-card>
                </template> 

            </b-table>
        </div>
    </v-card>
</template>

<script>
    import vSelect from 'vue-select';
    import 'vue-select/dist/vue-select.css';
    import { Store } from 'vuex';
    import Vue from 'vue';
    import api from "@/api"
    import { mapState } from 'vuex';
    import { 
        dispatchDeviceDataBind, 
        dispatchGetAwailableDevices,
        dispatchDeviceGetParams,
        dispatchGetAwailableDisplayDevices,
        dispatchRegisterDataBind,
        dispatchDeleteDatabind,
        dispatchUpdateDatabind
        } from '@/store/main/actions';
    import { 
        readDeviceDataBindList,
        readAvailableDevices,
        readDeviceParams,
        readAvailableDisplayDevices,
        readUpdateDatabindResponse
        } from '@/store/main/getters';

        Vue.component('v-select', vSelect);


    export default {
        data() {
            return {
                table_fields: [
                    {key: "id", sortable: true}, 
                    {key: "binder_name", sortable: true}, 
                    {key: "device_name", label: "Device name", sortable: true},
                    {key: "device_prop", sortable: true},
                    {key: "subscriber_name", label: "Subscriber name",sortable: true},
                    {key: "char_placeholder", label: "Placeholder", sortable: true},
                    {key: 'actions', label: 'Actions'},
                ],
                table_items: [],
                nonRegSortBy: 'id',
                nonRegSortDesc: true,
                currentItem: [],
                registered_devices: [],

                display_devices_list: [],
                selected_device: null,

                device_params: [],
                selected_param: null,

                selected_subscriber: null,
                
                placeholder_lenght: 1,
                databind_name_input: "",

                update_button_inactive: false,
                databind_selected_to_delete: null
            }
        },

        mounted() {
            // called for initiate the list of devices load from api 
            dispatchDeviceDataBind(this.$store)
            dispatchGetAwailableDevices(this.$store)
            dispatchGetAwailableDisplayDevices(this.$store)
        },

        methods: {
            validateState(ref) {
                if (
                    this.veeFields[ref] &&
                    (this.veeFields[ref].dirty || this.veeFields[ref].validated)
                ) {
                    return !this.veeErrors.has(ref);
                }
                return null;
            },
            deviceNameUpdate() {
                try {
                    if (this.table_items[0].device_uuid != null && this.registered_devices[0].name != null) {
                        let databind_list = JSON.parse(JSON.stringify(this.table_items));
                        for (let [index, val] of this.table_items.entries()) {
                            databind_list[index].device_name = this.getDeviceByUUID(val.device_uuid).name  
                            databind_list[index].subscriber_name = this.getDeviceByUUID(val.subscriber_uuid).name
                        }
                    this.table_items = databind_list
                    }
                    
                }
                catch (err) {
                }   
                
            },

            

            getDeviceByUUID(uuid) {
                let device;
                for (let item of this.registered_devices) {
                    if (item.uuid === uuid) {
                        device = item
                        break
                    }
                    else {
                        device = 'Unknown'
                    }
                }

                return device
            },

            getDisplayDeviceByUUID(uuid) {
                let device;
                for (let item of this.display_devices_list) {
                    if (item.uuid === uuid) {
                        device = item
                        break
                    }
                    else {
                        device = 'Unknown'
                    }
                }

                return device
            },

            onDeviceSelected() {
                dispatchDeviceGetParams(this.$store, this.selected_device.uuid);
            },

            registerDataBind() {
                this.$validator.validateAll().then((result) => {
                    if (!result) {
                        return;
                    }

                    let device_uuid = this.selected_device["uuid"]
                    let subscriber_uuid = this.selected_subscriber["uuid"]
                    let register_data_bind_obj = {
                        "binder_name": this.databind_name_input,
                        "device_uuid": device_uuid,
                        "device_prop": this.selected_param,
                        "subscriber_uuid": subscriber_uuid,
                        "char_placeholder": parseInt(this.placeholder_lenght)
                    }
                    dispatchRegisterDataBind(this.$store, register_data_bind_obj)
                    console.log(register_data_bind_obj)
                    this.invalidateSelectedValues();

                    this.$refs['create_databind_modal'].hide()
                });
                
            },

            registerDataBindReset() {
                this.invalidateSelectedValues();
                console.log("registerDataBindReset")
                this.$refs['create_databind_modal'].hide()
            },

            toggleDetailsRegistered(row) {
                console.log("toggleDetailsRegistered: " + JSON.stringify(row))

                this.databind_name_input = row.binder_name
                this.selected_device = this.getDeviceByUUID(row.device_uuid) 
                dispatchDeviceGetParams(this.$store, row.device_uuid);
                this.selected_param = row.device_prop
                this.selected_subscriber = this.getDisplayDeviceByUUID(row.subscriber_uuid) 
                this.placeholder_lenght = row.char_placeholder

                if(row._showDetails){
                this.$set(row, '_showDetails', false)
                }
                else{
                    this.currentItem.forEach(item => {
                        this.$set(item, '_showDetails', false)
                    })

                    this.$nextTick(() => {
                        this.$set(row, '_showDetails', true)
                    })
                }
            },

            updateDatabind(row) {
                this.$validator.validateAll().then((result) => {
                    if (!result) {
                        return;
                    }
                    this.update_button_inactive = true
                    let update_data_bind_obj = {
                        "id": row.id,
                        "binder_name": this.databind_name_input,
                        "device_uuid": this.selected_device["uuid"],
                        "device_prop": this.selected_param,
                        "subscriber_uuid": this.selected_subscriber["uuid"],
                        "char_placeholder": parseInt(this.placeholder_lenght)
                    }
                    console.log(update_data_bind_obj)
                    dispatchUpdateDatabind(this.$store, update_data_bind_obj)
                });
            },

            deleteDatabind(item) {
                this.databind_selected_to_delete = item
                console.log("DATABIND SELECTED TO DELETE: " + JSON.stringify(item.id))
                this.$refs['delete-databind-confirm'].show()
            },

            deleteDatabindAfterConfirm() {
                dispatchDeleteDatabind(this.$store, this.databind_selected_to_delete.id)
                this.databind_selected_to_delete = null
                this.$refs['delete-databind-confirm'].hide()
            },

            abortDeletingDatabind() {
                this.databind_selected_to_delete = null
                this.$refs['delete-databind-confirm'].hide()
            },

            invalidateSelectedValues() {
                this.selected_device = null
                this.selected_param = null
                this.device_params = []
                this.selected_subscriber = null
                this.databind_name_input = ""
                this.placeholder_lenght = 1
            }
        },

        computed: {
            readDeviceDataBindList: function(){
                return readDeviceDataBindList(this.$store)
            },

            readAvailableDevices: function(){
                return readAvailableDevices(this.$store)
            },

            readAvailableDisplayDevices: function(){
                return readAvailableDisplayDevices(this.$store)
            },
        
            readDeviceParams: function(){
                return readDeviceParams(this.$store)
            },

            readUpdateDatabindResponse: function(){
                return readUpdateDatabindResponse(this.$store)
            }
        },

        watch: {
            readDeviceDataBindList(newValue, oldValue) {
                this.table_items = newValue
                this.deviceNameUpdate()
            },

            readAvailableDevices(newValue, oldValue) {
                //on vuex parameter change - execute this function
                this.registered_devices = newValue
                this.deviceNameUpdate()
            },

            readAvailableDisplayDevices(newValue, oldValue) {
                this.display_devices_list = newValue
            },

            readDeviceParams(newValue, oldValue) {
                this.device_params = newValue.params
            },

            readUpdateDatabindResponse(newValue, oldValue) {
                this.update_button_inactive = false

                this.$validator.reset();
                this.invalidateSelectedValues()
                this.update_button_inactive = false
            }
        }
    }

</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .no_blink {
        caret-color: transparent;
    }

    .blink {
    caret-color: black;
}

    #create_data_bind_btn {
        float: right;
    }

    #device_selector, #device_parameter_selector, #subscriber_device_selector, #databind_placeholder_data_selector, #databind_name_input {
        width: 50%;
    }

    .registered_icons {
    margin-right: 30px
    }

    .databind_to_delete_fields {
    text-align: left;
    }

    #delete-decision-buttons-group {
        text-align: right;
    }

    #databind_table {
        margin-top: 50px
    }

    .databind_btn {
        float: right;
        margin-right: 15px;
    }

</style>