<template>
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
                                    @contextmenu="$emit('context_menu_clicked', $event, otp_data[row_idx][col_idx].databind_id)"
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
</template>

<script>
    import {commitAddNotification,} from '@/store/main/mutations';
    
    export default {
        data() {
            return{
                otp_id_devider: ":",
                hidden_subscribed_databinds: [],
            }    
        },
        props: {
            selected_display: null,
            otp_data: null,
            subscribed_databinds: null,
        },
        methods: {
            getDataBindNameById(binder_id) {
                if (binder_id != null) {
                    return this.subscribed_databinds.filter(s_binder => s_binder.id == binder_id)[0].binder_name
                }
            },
            getReservedCharsById(binder_id) {
                return this.subscribed_databinds.filter(s_binder => s_binder.id == binder_id)[0].char_placeholder
            },

            onDrop(evt, row_idx, col_idx) {
                const databindID = evt.dataTransfer.getData('databindID')
                console.log("onDrop: " + databindID)
                let can_be_dropped = this.canBeDropped(databindID, row_idx, col_idx)
                if (can_be_dropped.result) {
                    // remove databind from list
                    this.hidden_subscribed_databinds.push(databindID)
                    this.$emit("hidden_subscribed_databinds_update", this.hidden_subscribed_databinds)

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
        }
    } 
</script>

<style>
    .one_char_input {
        width: 40px;
        margin-left: 5px !important;
    }
</style>