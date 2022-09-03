<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3 no_blink" id="table_unregistered">
            <v-card-title primary-title>
                <div class="headline primary--text">Unregistered Sensors</div>
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

                    <template v-slot:cell()="data">
                        <span  v-b-tooltip.hover :title=returnToolTip(data.value)>{{ data.value}}</span>
                    </template>

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

                        <b-form-group id="sensor_select_location" label="Select sensor location:" label-for="sensor_location_selector" class="field_input" >
                            <v-select 
                                
                                id="sensor_location_selector"  
                                v-model="sensor_location_input" 
                                :options="sensor_locations" 
                                required 
                                placeholder="Select sensor_location"  
                                
                            >

                            </v-select>
                            <div v-if="sensor_location_input != null">
                                location selected: {{sensor_location_input.label}} 
                                <br>
                                description:  {{sensor_location_input.description}}
                            </div>
                        </b-form-group>

                        <br>

                        <b-button variant="primary" v-on:click = "register_sensor" v-bind:disabled="register_button_inactive">Register</b-button>
                    
                        </b-card>
                    </template>
                </b-table>    
            </div>
        </v-card>
        <v-card class="ma-3 pa-3 no_blink" id="table_registered">
            <v-card-title primary-title>
                <div class="headline primary--text">Registered Sensors</div>
            </v-card-title>
            <div>
                <b-table striped hover sort-icon-left
                    :items="table_items_registered" 
                    :fields="table_fields_registered" 
                    :sort-by.sync="sortBy"
                    :sort-desc.sync="sortDesc"
                    label-sort-asc=""
                    label-sort-desc=""
                    label-sort-clear=""
                    v-model="currentItems_registered">

                    <template v-slot:cell()="data">
                        <span  v-b-tooltip.hover :title=returnToolTip(data.value)>{{ data.value}}</span>
                    </template>
                    
                
                </b-table>
            </div>
        </v-card>
    </v-container>
    
</template>

<script>
    import vSelect from 'vue-select';
    import 'vue-select/dist/vue-select.css';
    import { Store } from 'vuex';
    import Vue from 'vue';
    import api from "@/api"
    import { mapState } from 'vuex';
    import { 
        dispatchedGetNotRegisteredSensors, 
        dispatchRegisterSensor, 
        dispatchSensorLocations,
        dispatchSensorTypes,
        dispatchedGetAwailableSensors 
        } from '@/store/main/actions';
    import { 
        readNotRegisteredSensors, 
        readSensorLocations,
        readSensorTypes,
        readAvailableSensors 
        } from '@/store/main/getters';

    Vue.component('v-select', vSelect);
    export default { 
 
    methods: {
        register_sensor: function(){
            this.is_type_updated = false 
            this.is_location_updated = false  
            this.register_button_inactive = true
            let register_sensor_obj = {
                "uuid": this.sensor_uuid,
                "name": this.sensor_name_input,
                "location": this.sensor_location_input.id
            }
            // perform api call to register sensor
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
        },
        typeUpdate() {
            // iterate over the all sensors
            console.log("typeUpdate()")
            
            let unreg_sensors_arr = JSON.parse(JSON.stringify(this.table_items));
            console.log("unreg_sensors_arr: " + JSON.stringify(unreg_sensors_arr))
            for (let [index, val] of this.table_items.entries()) {
                unreg_sensors_arr[index].type = this.getTypeAttrById(val.type)  
            }
            this.table_items = unreg_sensors_arr

            let registered_sensors_arr = JSON.parse(JSON.stringify(this.table_items_registered));
            for (let [index, val] of this.table_items_registered.entries()) {
                registered_sensors_arr[index].type = this.getTypeAttrById(val.type)  
            }
            this.table_items_registered = registered_sensors_arr
            
        },
       
        getTypeAttrById(id) {
            // iterate over the all sensor types. When found - return name, else return id
            let type_by_id;
            for (let item of this.sensor_types) {
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
            let registered_sensors_arr = JSON.parse(JSON.stringify(this.table_items_registered));
            for (let [index, val] of this.table_items_registered.entries()) {
                registered_sensors_arr[index].location = this.getLocationAttrById(val.location)  
            }
            this.table_items_registered = registered_sensors_arr
        },

        getLocationAttrById(id) {
            // iterate over the all sensor types. When found - return name, else return id
            let location_by_id;
            for (let item of this.sensor_locations_api) {
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

        returnToolTip(item_name) {
            let descr_by_name;
            for (let item of this.sensor_types) {
                if (item.name === item_name) {
                    descr_by_name = item.description
                    break
               }
               else {
                    for (let item of this.sensor_locations_api) {
                        if (item.name === item_name) {
                            descr_by_name = item.description
                            break
                        }
                        else {
                                descr_by_name = null
                        }   
                    }
               }   
            }
            return descr_by_name
        }, 
    },

   computed: {
        //need to define computed and watch function with the same name to watch vuex changes
        readNotRegisteredSensors: function(){
            return readNotRegisteredSensors(this.$store)
        },
        readAvailableSensors: function(){
            return readAvailableSensors(this.$store)
        },
        readSensorLocations: function(){
            return readSensorLocations(this.$store)
        },
        readSensorTypes: function(){
            return readSensorTypes(this.$store)
        }
        
   },
   
   watch: {
        readNotRegisteredSensors(newValue, oldValue) {
            //on vuex parameter change - execute this function
            var not_registered_sensors_arr = []
            newValue.forEach(element => {
                var list_obj = {uuid: element.uuid, first_occurrence: element.first_occurrence, type: element.type}
                not_registered_sensors_arr.push(list_obj)
            });

            this.table_items = not_registered_sensors_arr
            this.register_button_inactive = false
            this.typeUpdate()
        },
        readAvailableSensors(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.table_items_registered = newValue
        },
        readSensorLocations(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.sensor_locations_api = newValue

            var sensor_locations_arr = []
            newValue.forEach(element => {
                var list_obj = {label: element.name, id: element.location_id, description: element.description}
                sensor_locations_arr.push(list_obj)
            });
            
            this.sensor_locations = sensor_locations_arr
        },
        readSensorTypes(newValue, oldValue) {
            //on vuex parameter change - execute this function
            this.sensor_types = newValue
        },
        
    },

    data() {
        return {
            register_button_inactive: false,

            sensor_uuid: '',
            sensor_name_input: '',
            sensor_location_input: null,

            sensor_locations: [],
            sensor_locations_api: [],
            sensor_types: [],
            
            sortBy: 'first_occurrence',
            sortDesc: false,

            is_type_updated: false,
            is_location_updated: false,

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
            not_registered_sensors: false,
           
        }
    },
  
    mounted() {
        //called for initiate the list of sensors load from api 
        dispatchedGetNotRegisteredSensors(this.$store)
        dispatchSensorLocations(this.$store)
        dispatchSensorTypes(this.$store)
        dispatchedGetAwailableSensors(this.$store)
    },

    beforeDestroy() {
        this.is_type_updated = false 
        this.is_location_updated = false 
    },

    updated() { 
        // when all items loaded and not null - update sensor type to string format (sensor_type is another api)
        console.log('updated()')
        try { 
            if (this.table_items[0].type != null && this.sensor_types[0].type_id != null && this.table_items_registered[0].type != null && !this.is_type_updated) {
                this.typeUpdate()
                this.is_type_updated = true
            }
            
        }
        catch (err) {
        }

        try { 
            if (this.sensor_locations_api[0].location_id != null && this.table_items_registered[0].location && !this.is_location_updated) {
                this.locationUpdate()
                this.is_location_updated = true
            }
            
        }
        catch (err) {
        }
    }
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
</style>
