<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
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
                        :options="device_select" 
                        required 
                        placeholder="Select device"  
                        @open="on_open_device_selector"
                    >

                    </v-select>

                </b-form-group>

                <v-select
                    v-model="compress_ratio"
                    :reduce="(option) => option.id"
                    :options="[
                    { label: '0', id: 0 },
                    { label: '1', id: 1 },
                    { label: '2', id: 2 },
                    
                    ]"
                    :clearable=false
                />
 

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

        
    </v-container>
</template>


<script>
import { Store } from 'vuex';
import { readAvailableDevices, readCompressDb } from '@/store/main/getters';
import { dispatchGetAwailableDevices, dispatchedCompressDb } from '@/store/main/actions';
import Vue from 'vue';
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';
import api from "@/api"
import { mapState } from 'vuex';
Vue.component('v-select', vSelect);



export default { 
 
    methods: {
        compress_db(value){
            let compress_payload = {
                "start_date_time": this.value_date_from + " " + this.time_value_from,
                "end_date_time": this.value_date_to + " " + this.time_value_to,
                "for_items_with_compress_ratio": this.compress_ratio,
                "uuid": this.selected_device.value
            }
           
            console.log(compress_payload)
            dispatchedCompressDb(this.$store, compress_payload)
           
            this.spinner_visible=true
            this.button_inactive=true

        },

        get_device_list() {
            // get devices from api and parse it for Vue Select
            var parsedobj = JSON.parse(JSON.stringify(readAvailableDevices(this.$store)))
            var device_list_array = []
        
            parsedobj.forEach(element => {
                var list_obj = {value: element.uuid, label: element.name}
                device_list_array.push(list_obj)
            });
            this.device_select = device_list_array

        },

        on_open_device_selector () {
            //defined in template part
            //triggered each time when select_device is opened
            this.get_device_list()
        },

       
    },

   computed: {
    //need to define computed and watch function with the same name to watch vuex changes
    compressDbResponse: function(){
      return readCompressDb(this.$store)
    }
  },
   
   watch: {
        compressDbResponse(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.showDismissibleAlert = true
            this.response_compress_db = newValue.items_selected_to_compress
            this.spinner_visible=false
            this.button_inactive=false
        }
    },

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
            
            device_select: [],
            response_compress_db: '',
            showDismissibleAlert: false
        }
    },
  
    mounted() {
        // called for initiate the list of devices load from api 
        dispatchGetAwailableDevices(this.$store)
        
    },

    beforeDestroy() {
        
            
    },

    updated() {
        if (this.spinner_visible == false) {
            if (this.value_date_from != "" & this.value_date_to != "" & this.time_value_from != "" & this.time_value_to != "" & this.selected_device != "" ) {
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