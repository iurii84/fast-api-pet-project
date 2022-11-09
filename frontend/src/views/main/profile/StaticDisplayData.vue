<template>
    <v-card class="ma-5 pa-5">
        <v-card-title primary-title>
            <div class="headline primary--text">Static Display Data</div>
        </v-card-title>

        <v-menu
            v-model="show_context_menu"
            :position-x="context_menu_x"
            :position-y="context_menu_y"
            absolute
            offset-y>

            <v-list>
                <v-list-item
                @click="onClickRemoveDatabind()">
                    <v-list-item-title>Remove databind...</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>

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
                    <div>
                        <v-badge
                                    color="green"
                                    v-bind:hidden="isSubscribedDatabindHidden(n.id)"
                                    :content="n.char_placeholder"
                                    v-for="n in subscribed_databinds"
                                    overlap
                                    offset-x="15"
                                    offset-y="15"
                                    >
                            <v-chip
                                class="ma-2"
                                draggable
                                :key="n.binder_name"
                                @dragstart="startDrag($event, n)">
                                    {{n.binder_name}}   
                            </v-chip>
                        </v-badge>
                    </div>

                    <v-spacer class="ma-12"></v-spacer>

                    <div v-if="selected_display != null">
                        <v-form>
                            <v-container>
                                <v-row
                                    v-for="display_row, row_idx in selected_display.json.display_height"
                                    >
                                    <span
                                        v-for="display_col, col_idx in selected_display.json.display_width"
                                        class="one_char_input"
                                        >
                                        <v-tooltip
                                            top
                                            :disabled="otp_data[row_idx][col_idx].databind_id == null">
                                            <template v-slot:activator="{ on, attrs }">
                                                <div
                                                    v-bind="attrs" 
                                                    v-on="on"
                                                    @contextmenu="context_menu_show($event, otp_data[row_idx][col_idx].databind_id)"
                                                    :ripple="false">
                                                    <v-otp-input
                                                        :id=[row_idx]+[otp_id_devider]+[col_idx]
                                                        v-model="otp_data[row_idx][col_idx].letter"
                                                        :set="state = otp_data[row_idx][col_idx].disabled"
                                                        v-bind:dark="state"
                                                        v-bind:disabled="state"
                                                        length="1"
                                                        @drop="onDrop($event, row_idx, col_idx)"
                                                        @dragover.prevent
                                                        @dragenter.prevent
                                                        >
                                                    </v-otp-input>
                                                </div>
                                            </template>
                                            <span>
                                                {{getDataBindNameById(otp_data[row_idx][col_idx].databind_id)}}
                                            </span>
                                        </v-tooltip>    
                                    </span>   
                                </v-row>
                            </v-container>  
                        </v-form>
                    </div>
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

    import {
        commitAddNotification,
    } from '@/store/main/mutations';

    export default {
        data () {
            return {
                step: 1,
                otp_data: null,
                otp_id_devider: ":",
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
            getReservedCharsById(binder_id) {
                return this.subscribed_databinds.filter(s_binder => s_binder.id == binder_id)[0].char_placeholder
            },

            getDataBindNameById(binder_id) {
                if (binder_id != null) {
                    return this.subscribed_databinds.filter(s_binder => s_binder.id == binder_id)[0].binder_name
                }
            },
            
            startDrag(evt, item) {
                console.log("startDrag")
                evt.dataTransfer.dropEffect = 'move'
                evt.dataTransfer.effectAllowed = 'move'
                evt.dataTransfer.setData('databindID', item.id)
            },
            onDrop(evt, row_idx, col_idx) {
                const databindID = evt.dataTransfer.getData('databindID')
                console.log("onDrop: " + databindID)
                let can_be_dropped = this.canBeDropped(databindID, row_idx, col_idx)
                if (can_be_dropped.result) {
                    // remove databind from list
                    this.hidden_subscribed_databinds.push(databindID)

                    // disable and make unavailable fields
                    // unavailable adds 1 reserved field on each side of disabled fields
                    // assign databind_id
                    let occupied_cells = this.getReservedCharsById(databindID)
                    for (let i = 0; i < occupied_cells; i++) {
                        this.otp_data[row_idx][col_idx + i].disabled = true
                        this.otp_data[row_idx][col_idx + i].databind_id = databindID
                    }

                    for (let i = 0; i < occupied_cells + 2; i++) {
                        let index = col_idx - 1 + i
                        if (index >= 0 && index < 20) {
                            this.otp_data[row_idx][index].unavailable = true
                        }  
                    }
                    
                }
                else {
                    console.log("CAN NOT BE DROPPED: " + can_be_dropped.err_validation)
                    commitAddNotification(this.$store, { content: 'CAN NOT BE DROPPED: ' + can_be_dropped.err_validation, color: 'error' });
                }
                
            },
            canBeDropped(databind_id, row_idx, col_idx) {
                // check if subscriber can be dropped on display
                // if it's inside display, if it's not intersected with other subscribers
                let display_params = this.selected_display.json
                let display_width = display_params.display_width
                let display_height = display_params.display_height
                let self_reserved_chars = this.getReservedCharsById(databind_id)

                let can_be_dropped = true
                let err_validator = ""

                // now each verification can set returned value to false
                if (self_reserved_chars + col_idx > display_width) {
                    can_be_dropped = false
                    err_validator = "you are trying to place the binder outside of the display"
                }
                
                for (let i = 0; i < self_reserved_chars; i++){
                    let index = col_idx + i
                    if (index >= 0 && index < 20) {
                        if (this.otp_data[row_idx][index].unavailable) {
                            can_be_dropped = false
                            err_validator = "the binder is intersected with already placed binders or you should have at least 1 space between the binders"
                        }
                        if (this.otp_data[row_idx][index].letter != "") {
                            can_be_dropped = false
                            err_validator = "the binder is intersected with the text"
                        }
                    }
                }

                return {"result": can_be_dropped, "err_validation": err_validator}
            },
            isSubscribedDatabindHidden(databind_id) {
                let is_hidden = this.hidden_subscribed_databinds.findIndex(item => item == databind_id) > -1; 
                return is_hidden
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