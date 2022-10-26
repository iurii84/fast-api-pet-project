<template>
    <v-card class="ma-5 pa-5">
        <v-card-title primary-title>
            <div class="headline primary--text">Static Display Data</div>
        </v-card-title>

        <v-stepper
            v-model="step"
            vertical
        >
            <v-stepper-step
                :complete="step > 1"
                step="1"
            >
                Select display device
                <small>You are going to create static display data for selected display device</small>
            </v-stepper-step>
  
            <v-stepper-content step="1">
                <v-card
                    class="mb-12"
                    height="200px"
                >
                    <v-select
                        :items="display_devices_list"
                        v-model="selected_display"
                        @change="onDisplaySelected"
                        solo
                        item-text=name
                        return-object
                    >

                    </v-select>
               
                    <div v-if="selected_display">
                        ID: {{selected_display.id}}
                        <br>
                        UUID: {{selected_display.uuid}}
                        <br>
                        TYPE: {{getDeviceTypeById(selected_display.type).name}}
                        <br>
                        LOCATION: {{getDeviceLocationById(selected_display.location).name}}
                    </div>
                </v-card>
                <v-btn
                    color="primary"
                    @click="step = 2"
                >
                    Continue
                </v-btn>

                <v-btn text>
                    Cancel
                </v-btn>
            </v-stepper-content>
  
            <v-stepper-step
                :complete="step > 2"
                step="2"
            >
                Configure analytics for this app
            </v-stepper-step>
        
            <v-stepper-content step="2">
                <v-card
                color="grey lighten-1"
                class="mb-12"
                height="200px"
                ></v-card>
                <v-btn
                color="primary"
                @click="step = 3"
                >
                Continue
                </v-btn>
                <v-btn text>
                Cancel
                </v-btn>
            </v-stepper-content>
        
            <v-stepper-step
                :complete="step > 3"
                step="3"
            >
                Select an ad format and name ad unit
            </v-stepper-step>
        
            <v-stepper-content step="3">
                <v-card
                color="grey lighten-1"
                class="mb-12"
                height="200px"
                ></v-card>
                <v-btn
                color="primary"
                @click="step = 4"
                >
                Continue
                </v-btn>
                <v-btn text>
                Cancel
                </v-btn>
            </v-stepper-content>
        
            <v-stepper-step step="4">
                View setup instructions
            </v-stepper-step>
            <v-stepper-content step="4">
                <v-card
                color="grey lighten-1"
                class="mb-12"
                height="200px"
                ></v-card>
                <v-btn
                color="primary"
                @click="step = 1"
                >
                Continue
                </v-btn>
                <v-btn text>
                Cancel
                </v-btn>
            </v-stepper-content>
        </v-stepper>
    </v-card>
</template>

<script>
    import { 
        dispatchDeviceLocations,
        dispatchDeviceTypes,
        dispatchGetAwailableDisplayDevices,
        
        } from '@/store/main/actions';

    import { 
        readAvailableDisplayDevices, 
        readDeviceLocations, 
        readDeviceTypes,
        
        } from '@/store/main/getters';


    export default {
        data () {
            return {
                step: 1,

                device_locations: null,
                device_types: null,

                display_devices_list: null,
                selected_display: null
            }
        },
        mounted() {
                // called for initiate the list of devices load from api 
                dispatchGetAwailableDisplayDevices(this.$store)
                dispatchDeviceLocations(this.$store)
                dispatchDeviceTypes(this.$store)
            },

        methods: {
            onDisplaySelected() {
                console.log("onDisplaySelected")
            },

            getDeviceTypeById(id) {
                let device_type;
                for (let item of this.device_types) {
                    if (item.type_id === id) {
                        device_type = item
                        break
                    }
                    else {
                        device_type = 'Unknown'
                    }
                }

                return device_type
            },

            getDeviceLocationById(id) {
                let device_location;
                for (let item of this.device_locations) {
                    if (item.location_id === id) {
                        device_location = item
                        break
                    }
                    else {
                        device_location = 'Unknown'
                    }
                }

                return device_location
            }
        },

        computed: {
            readAvailableDisplayDevices: function(){
                return readAvailableDisplayDevices(this.$store)
            },
            readDeviceLocations: function(){
                return readDeviceLocations(this.$store)
            },
            readDeviceTypes: function(){
                return readDeviceTypes(this.$store)
            },
        
        },

        watch: {
            readAvailableDisplayDevices(newValue, oldValue) {
                this.display_devices_list = newValue;
            },
            readDeviceLocations(newValue, oldValue) {
            //on vuex parameter change - execute this function
                this.device_locations = newValue;
            },
            readDeviceTypes(newValue, oldValue) {
            //on vuex parameter change - execute this function
                this.device_types = newValue;
            },

        }
    }
</script>