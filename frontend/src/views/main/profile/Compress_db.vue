<template>
    <v-card class="ma-5 pa-5">
        <v-card-title primary-title>
            <div class="headline primary--text">Compress DB</div>
        </v-card-title>

        <div>
            <b-alert v-model="showDismissibleAlert" variant="success" dismissible>
                <h4 class="alert-heading">Database was successfully compressed! </h4>
                <hr>
                <p class="mb-0">
                    {{ response_compress_db }} records were deleted!
                    <br>
                    Timeline coverage  
                    <br>
                    <b>from: </b>  {{value_date_from}}  {{time_value_from}}   
                    <br>
                    <b>to:</b> &nbsp; &nbsp; &nbsp;{{value_date_to}}  {{time_value_to}}
                </p> 
            </b-alert>
        </div>

        <div>
            <b-form id='compress_db_form' @submit.stop.prevent="compress_db"  >
                <b-form-group id="device_select" label="Select device:" label-for="device_select_form" >
                    <v-select 
                        id="device_select_form"  
                        v-model="selected_device" 
                        :items="registered_devices" 
                        item-text=name
                        required 
                        placeholder="Select device"  
                        return-object
                    >
                    </v-select>

                </b-form-group>

                <b-form-group id="compress_ratio_select" label="Select compress ratio:" label-for="compress_select_ratio_form" >
                    <v-select
                        id="compress_select_ratio_form"
                        v-model="compress_ratio"
                        :items="[
                            { text: '0', id: 0 },
                            { text: '1', id: 1 },
                            { text: '2', id: 2 },
                        ]"
                    />
                </b-form-group>
                
                <div class="date_time_container">
                    <span class="date_time">
                        <div>
                            <label for="datepicker_from">Date from:</label>
                            <b-form-datepicker 
                                id="datepicker_from" 
                                form="compress_db_form"
                                v-model="value_date_from" 
                                required
                                >
                            </b-form-datepicker>

                            <br>
                            
                            <label for="timepicker_from">Time from:</label>
                            <b-col md="auto">
                                <b-form-timepicker 
                                    id="timepicker_from" 
                                    v-model="time_value_from"  
                                    :hour12=false 
                                    :no-close-button=true
                                    :hide-header=true
                                    required
                                    >
                                </b-form-timepicker>
                            </b-col>
                        </div>
                    </span>

                    <span class="date_time">
                        <div>
                            <label for="datepicker_to">Date to:</label>
                            <b-form-datepicker 
                                id="datepicker_to" 
                                v-model="value_date_to" 
                                required
                                >
                            </b-form-datepicker>
                            
                            <br>

                            <label for="timepicker_to">Time to:</label>
                            <b-col md="auto">
                                <b-form-timepicker 
                                    id="timepicker_to" 
                                    v-model="time_value_to"  
                                    :hour12=false
                                    :no-close-button=true
                                    :hide-header=true
                                    required
                                >
                                </b-form-timepicker>
                            </b-col>
                        </div>
                    </span>
                </div>
            
                <b-button type="submit" variant="primary" v-bind:disabled="button_inactive">
                    <b-spinner small v-if="spinner_visible"></b-spinner>
                    Compress DB
                </b-button>
            </b-form>
        </div>
    </v-card>
</template>


<script>
    import { Store } from 'vuex';
    import { 
        readAvailableDevices, 
        readCompressDb } from '@/store/main/getters';
    import { 
        dispatchGetAwailableDevices, 
        dispatchCompressDb, 
        dispatchGetTask } from '@/store/main/actions';
    import Vue from 'vue';
    import api from "@/api"
    import { mapState } from 'vuex';


    export default { 
        data() {
            return {
                value_date_from: '',
                value_date_to: '',
                time_value_from: '',
                time_value_to: '',
                
                spinner_visible: false,
                button_inactive: true,
                compress_ratio: 0,
                show: true,
                selected_device: "",
                
                registered_devices: [],
                response_compress_db: '',
                showDismissibleAlert: false
            }
        },
    
        methods: {
            compress_db(value){
                let compress_payload = {
                    "start_date_time": this.value_date_from + " " + this.time_value_from,
                    "end_date_time": this.value_date_to + " " + this.time_value_to,
                    "for_items_with_compress_ratio": this.compress_ratio,
                    "uuid": this.selected_device.uuid
                }
            
                console.log(compress_payload)
                dispatchCompressDb(this.$store, compress_payload)
            
                this.spinner_visible=true
                this.button_inactive=true

            },
        },

        computed: {
                //need to define computed and watch function with the same name to watch vuex changes
                compressDbResponse: function(){
                return readCompressDb(this.$store)
                },

                readAvailableDevices: function(){
                    return readAvailableDevices(this.$store)
                },
        },
        
        watch: {
                compressDbResponse(newValue, oldValue) {
                    //on vuex parameter change - execute this function
                    dispatchGetTask(this.$store, newValue.task_id)
                    this.showDismissibleAlert = true
                    this.response_compress_db = newValue.items_selected_to_compress
                    this.spinner_visible=false
                    this.button_inactive=false
                },

                readAvailableDevices(newValue, oldValue) {
                    //on vuex parameter change - execute this function
                    this.registered_devices = newValue
                
                },
            },

        
    
        mounted() {
            // called for initiate the list of devices load from api 
            dispatchGetAwailableDevices(this.$store)
        },

        updated() {
            if (this.spinner_visible == false) {
                if (
                    this.value_date_from != "" 
                    & this.value_date_to != "" 
                    & this.time_value_from != "" 
                    & this.time_value_to != "" 
                    & this.selected_device != "" ) {
                        this.button_inactive=false;
                }    
            }    
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.date_time_container {
  display: flex; 
  justify-content: left; 
}

.date_time {
    padding: 20px;
}

#device_select {
    padding-bottom: 3%;
}

</style>