<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
        <v-card-title primary-title>
            <div class="headline primary--text">Compress DB</div>
        </v-card-title>

        <div>
            <b-form id='compress_db_form' @submit.stop.prevent="compress_db"  >
                <b-form-group id="sensor_select" label="Select sensor:" label-for="sensor_select_form" >
                    <v-select 
                        
                        id="sensor_select_form"  
                        v-model="selected_sensor" 
                        :options="sensor_select" 
                        required 
                        placeholder="Select sensor"  
                        @open="on_open_sensor_selector"
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
                        <p>Value: '{{ value_date_from }}'</p>

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
                        <p>Value: '{{ value_date_to }}'</p>

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
import { readAvailableSensors } from '@/store/main/getters';
import { dispatchedGetAwailableSensors } from '@/store/main/actions';
import Vue from 'vue';
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';
import api from "@/api"
Vue.component('v-select', vSelect);



export default { 
 
    methods: {
        compress_db(value){
            let compress_payload = {
                "start_date_time": this.value_date_from + " " + this.time_value_from,
                "end_date_time": this.value_date_to + " " + this.time_value_to,
                "for_items_with_compress_ratio": this.compress_ratio,
                "uuid": this.selected_sensor.value
            }
           
            console.log(compress_payload)
           
            this.spinner_visible=true
            this.button_inactive=true
        },

        get_sensor_list() {
            //get sensors from api and parse it for Vue Select
            var parsedobj = JSON.parse(JSON.stringify(readAvailableSensors(this.$store)))
            var sensor_list_array = []
        
            parsedobj.forEach(element => {
                var list_obj = {value: element.uuid, label: element.name}
                sensor_list_array.push(list_obj)
            });
            this.sensor_select = sensor_list_array

        },

        on_open_sensor_selector () {
            //defined in template part
            //triggered each time when select_sensor is opened
            this.get_sensor_list()
        },
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
            selected_sensor: "",
            sensors_get_result: [],
            sensor_select: []
        }
    },
  
    mounted() {
        //called for initiate the list of sensors load from api 
        dispatchedGetAwailableSensors(this.$store)
        
    },

    beforeDestroy() {
        
            
    },

    updated() {
        if (this.spinner_visible == false) {
            if (this.value_date_from != "" & this.value_date_to != "" & this.time_value_from != "" & this.time_value_to != "" & this.selected_sensor != "" ) {
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

#sensor_select {
    padding-bottom: 3%;
}




</style>