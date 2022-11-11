<template>
    <v-card class="ma-5 pa-5">
        <v-card-title primary-title>
            <div class="headline primary--text">Static Display Data</div>
        </v-card-title>

        <ContextMenuRemoveDatabind
            :position_x="context_menu_x"
            :position_y="context_menu_y"
            :show="show_context_menu"
            @removeDatabindClicked="onClickRemoveDatabind()">
        </ContextMenuRemoveDatabind>

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
                    height="400px"
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

                    <b-form-group id="display_frame_name_input_group" label="Display frame name:" label-for="display_frame_name_input"  >
                        <b-form-input
                                id="display_frame_name_input"
                                v-model="display_name"
                                type="text" >
                        </b-form-input>
                    </b-form-group>

                    <b-form-group id="display_frame_priority_input_group" label="Display frame priority:" label-for="display_frame_priority_input"  >
                        <b-form-input
                                id="display_frame_priority_input"
                                v-model="display_priority"
                                type="number" >
                        </b-form-input>
                    </b-form-group>
               
                    <div 
                        v-if="selected_display"
                        id="display_info_section">
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
                Drag&drop databinds to display:
            </v-stepper-step>
        
            <v-stepper-content step="2">
                <v-card
                    class="mb-12"
                    height="400px"
                    >
                    <v-spacer class="ma-2"></v-spacer>
                    
                    <DatabindDraggableItems
                        :subscribed_databinds="subscribed_databinds"
                        :hidden_subscribed_databinds="hidden_subscribed_databinds"
                        @databind_drag_start="startDrag">
                    </DatabindDraggableItems>

                    <v-spacer class="ma-12"></v-spacer>

                    <Screen
                        :selected_display="selected_display"
                        :otp_data="otp_data"
                        :subscribed_databinds="subscribed_databinds"
                        @context_menu_clicked="context_menu_show"
                        @hidden_subscribed_databinds_update="(updated_hidden) => hidden_subscribed_databinds = updated_hidden">
                    </Screen>
                    
                </v-card>
                <v-btn
                    color="primary"
                    @click="post_display_data()"
                    >
                Continue
                </v-btn>
                <v-btn 
                    text
                    @click="step = 1">
                Back
                </v-btn>
                <v-btn 
                    text
                    @click="clearDisplay"
                    color="warning">
                Clear display
                </v-btn>
            </v-stepper-content>
        
            <v-stepper-step
                :complete="step > 3"
                step="3"
            >
                Drag&drop blocks to display:
            </v-stepper-step>
        
            <v-stepper-content step="3">
                <v-card
                    class="mb-12"
                    height="400px"
                >
                    
                </v-card>
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
        dispatchSubscribedDataBind,
        dispatchRegisterStaticDisplayFrame
        } from '@/store/main/actions';

    import { 
        readAvailableDisplayDevices, 
        readDeviceLocations, 
        readDeviceTypes,
        readSubscribedDataBindList,
        } from '@/store/main/getters';

    

    import ContextMenuRemoveDatabind from '@/views/main/profile/StaticDisplayDataComponents/ContextMenuRemoveDatabind.vue';
    import DatabindDraggableItems from '@/views/main/profile/StaticDisplayDataComponents/DatabindDraggableItems.vue';
    import Screen from '@/views/main/profile/StaticDisplayDataComponents/Screen.vue';

    export default {
        data () {
            return {
                step: 1,
                otp_data: null,
                
                hidden_subscribed_databinds: [],
                display_name: null,
                display_priority: null,

                device_locations: null,
                device_types: null,

                display_devices_list: null,
                selected_display: null,

                subscribed_databinds: null,

                show_context_menu: false,
                context_menu_x: 0,
                context_menu_y: 0,
                context_selected_databind: null,  
            }
        },
        components: {
            ContextMenuRemoveDatabind,
            DatabindDraggableItems,
            Screen
        },
        mounted() {
                // called for initiate the list of devices load from api 
                dispatchGetAwailableDisplayDevices(this.$store)
                dispatchDeviceLocations(this.$store)
                dispatchDeviceTypes(this.$store)
                this.generate_otp_obj()
            },

        methods: {
            generate_backend_obj() {
                return {
                    "device_uuid": this.selected_display.uuid,
                    "frame_name": this.display_name,
                    "frame_priority": this.display_priority,
                    "data_json": this.otp_data,
                    "placed_databinds": this.hidden_subscribed_databinds,
                    "is_active": false
                }

            },
            post_display_data() {
                let be_data = this.generate_backend_obj()
                console.log(be_data)
                dispatchRegisterStaticDisplayFrame(this.$store, be_data)
            },
            onClickRemoveDatabind() {
                // remove databind by id from screen
                if (this.context_selected_databind != null) {
                    // remove from hidden list
                    const index = this.hidden_subscribed_databinds.indexOf(this.context_selected_databind);
                    if (index !== -1) {
                        this.hidden_subscribed_databinds.splice(index, 1);
                    }

                    let taken_positions = [];
                    let taken_line = null;
                    
                    // find all positions on screen
                    this.otp_data.forEach((line, ln_index) => {
                        line.forEach((item, item_index) => {
                            if (item.databind_id === this.context_selected_databind) {
                                taken_positions.push(item_index)
                                taken_line = ln_index
                            }
                        });
                    });

                    // clear parameters for found positions + 1 position before and 1 position after
                    for (let i = -1; i < taken_positions.length + 2; i++) {
                        if (this.otp_data[taken_line][i + taken_positions[0]] != null) {
                            this.otp_data[taken_line][i + taken_positions[0]].disabled = false;
                            this.otp_data[taken_line][i + taken_positions[0]].unavailable = false;
                            this.otp_data[taken_line][i + taken_positions[0]].databind_id = null;
                        }
                    }
                }
            },

            context_menu_show (e, databind_id) {
                // show context menu if 'context_selected_databind' is not null
                console.log("context_menu_show")
                this.context_selected_databind = databind_id
                e.preventDefault()
                this.show_context_menu = false
                this.context_menu_x = e.clientX
                this.context_menu_y = e.clientY
                this.$nextTick(() => {
                    if (this.context_selected_databind) {
                        this.show_context_menu = true
                    }
                })
            },
            generate_otp_obj() {
                // generate empty otp obj
                let otp_obj = []

                for (let i = 0; i < 4; i++) {
                    let otp_line = [];
                    for (let i = 0; i < 20; i++){
                        otp_line.push({
                            "letter": '', 
                            "disabled": false,
                            "unavailable": false,
                            "databind_id": null})
                    }
                    otp_obj.push(otp_line)
                }
                this.otp_data = otp_obj
            },
            clearDisplay() {
                console.log("Clear display...")
                this.clearBindHiddenStatusList();
                this.generate_otp_obj()
            },
            
            clearBindHiddenStatusList() {
                this.hidden_subscribed_databinds.splice(0)
            },
            
            startDrag(evt, item) {
                console.log("startDrag")
                console.log(evt)
                console.log(item)
                evt.dataTransfer.dropEffect = 'move'
                evt.dataTransfer.effectAllowed = 'move'
                evt.dataTransfer.setData('databindID', item.id)
            },
            
            
            onDisplaySelected() {
                console.log("onDisplaySelected")
                dispatchSubscribedDataBind(this.$store, this.selected_display.uuid)
            },

            getDeviceTypeById(id) {
                return this.device_types.filter(type => type.type_id === id)[0]
            },

            getDeviceLocationById(id) {
                return this.device_locations.filter(location => location.location_id === id)[0]
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
            readSubscribedDataBindList: function(){
                return readSubscribedDataBindList(this.$store)
            },
        
        },

        watch: {
            readAvailableDisplayDevices(newValue, oldValue) {
                //on vuex parameter change - execute this function
                this.display_devices_list = newValue;
            },
            readDeviceLocations(newValue, oldValue) {
                this.device_locations = newValue;
            },
            readDeviceTypes(newValue, oldValue) {
                this.device_types = newValue;
            },
            readSubscribedDataBindList(newValue, oldValue) {
                this.subscribed_databinds = newValue
            }
        }
    }  
</script>

<style>
   .one_char_input {
    width: 40px;
    margin-left: 5px !important;
   }

   #display_frame_name_input_group {
    margin-top: 15px;
   }
</style>