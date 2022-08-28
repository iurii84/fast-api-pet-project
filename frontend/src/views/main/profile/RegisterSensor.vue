<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
            <div class="headline primary--text">Register Sensor</div>
        </v-card-title>
        <div>
            <b-table striped hover sort-icon-left
                :items="table_items" 
                :fields="table_fields" 
                :sort-by.sync="sortBy"
                :sort-desc.sync="sortDesc"
                label-sort-asc=""
                label-sort-desc=""
                label-sort-clear=""
                v-model="currentItems">


                <template v-slot:cell(actions)="{ detailsShowing, item }" >
                    <!-- Use the built in method from the scoped data to toggle the row details -->
                    <b-btn @click="toggleDetails(item)">{{ detailsShowing ? 'Close' : 'Register sensor'}}</b-btn>
                </template>
                
                 <template v-slot:row-details="{ item }">
                    <b-card>
                    <label for="field_input_uuid" class="field_input">UUID: </label>
                    <b-form-input v-model="item.uuid"  disabled class="field_input" id="field_input_uuid"> 
                    {{sensor_uuid = item.uuid}}    
                    </b-form-input>

                    <br>
                    
                    <label for="field_input_sensor_name" class="field_input">Sensor name: </label>
                    <b-form-input v-model="sensor_name_input" placeholder="Sensor name" class="field_input" id="field_input_sensor_name">
                    </b-form-input>

                    <label for="field_input_sensor_location" class="field_input">Sensor location: </label>
                    <b-form-input v-model="sensor_location_input" type="number" class="field_input" id="field_input_sensor_location">
                    </b-form-input>

                    <br>

                    <b-button variant="primary" v-on:click = "register_sensor" v-bind:disabled="register_button_inactive">Register</b-button>
                 
                    </b-card>
                </template>
            </b-table>
            
            
                
        </div>

        </v-card>
    </v-container>
</template>

<script>
    import { Store } from 'vuex';
    import Vue from 'vue';
    import api from "@/api"
    import { mapState } from 'vuex';
    import { dispatchedGetNotRegisteredSensors, dispatchRegisterSensor } from '@/store/main/actions';
    import { readNotRegisteredSensors } from '@/store/main/getters';


    export default { 
 
    methods: {
        register_sensor: function(){
            this.register_button_inactive = true
            let register_sensor_obj = {
                "uuid": this.sensor_uuid,
                "name": this.sensor_name_input,
                "location": this.sensor_location_input
            }
            dispatchRegisterSensor(this.$store, register_sensor_obj)
            
            console.log(register_sensor_obj)
        },

        //finds a specific item based on the provided ID and toggles details on that item
        toggleDetails(row) {
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
        }
    },

   computed: {
        //need to define computed and watch function with the same name to watch vuex changes
        readNotRegisteredSensors: function(){
            return readNotRegisteredSensors(this.$store)
        }
   },
   
   watch: {
       readNotRegisteredSensors(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.table_items = newValue
            this.register_button_inactive = false
        }
    },

    data() {
        return {
            register_button_inactive: false,

            sensor_uuid: 'na',
            sensor_name_input: '',
            sensor_location_input: 0,

            sortBy: 'first_occurrence',
            sortDesc: false,

            currentItems: [],
            table_fields: [
                {key: "uuid", sortable: true}, 
                {key: "first_occurrence", sortable: true}, 
                {key: "type", sortable: true},
                {key: 'actions', label: 'Actions'},
            ],
            table_items: [],
            not_registered_sensors: false
        }
    },
  
    mounted() {
        //called for initiate the list of sensors load from api 
        dispatchedGetNotRegisteredSensors(this.$store)
        
    },

    beforeDestroy() {
               
    },

    updated() {
       
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.field_input {
    margin: 3px; 
    width: 50%;
    
}
</style>
