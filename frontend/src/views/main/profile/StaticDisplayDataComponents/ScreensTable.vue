<template>
    <div>
        <v-data-table
            v-if="static_display_data_list != null"
            :headers="headers"
            :items="static_display_data_list"
            :items-per-page="5"
            class="elevation-1"
            no-data-text="NO DATA"
            sort-by="id"
            sort-desc
            >

            <template v-slot:item.actions="{ item }">
                <v-icon
                    class="mr-2"
                    @click="editItem(item)"
                >
                    mdi-pencil
                </v-icon>

                <v-icon
                    @click="$emit('delete_static_frame', item.id)"
                >
                    mdi-delete
                </v-icon>
            </template>

        </v-data-table>
    </div>
</template>

<script>
    export default {
        props: {
            static_display_data_list: null,
        },
        data () {
            return {
                headers: [
                    {
                        text: 'ID',
                        width: '5%',
                        allign: 'start',
                        value: 'id'
                    },
                    { 
                        text: 'Frame name', 
                        value: 'frame_name' 
                    },
                    {
                        text: 'Device UUID',
                        value: 'device_uuid',
                    },
                    {
                        text: 'Frame priority',
                        value: 'frame_priority',
                    },
                    {
                        text: 'Is active',
                        value: 'is_active',
                    },
                    {
                        text: 'Placed databinds',
                        value: 'placed_databinds',
                    },
                    { 
                        text: 'Actions', 
                        value: 'actions', 
                        sortable: false 
                    },
                ],

                
            }
        }
    }

</script>