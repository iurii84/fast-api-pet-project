<template>
    <div>
        <v-badge
                color="blue"
                v-bind:hidden="isSubscribedDatabindHidden(databind.id)"
                :content="databind.char_placeholder"
                v-for="databind in subscribed_databinds"
                overlap
                offset-x="20"
                offset-y="20"
                >
            <v-chip
                class="ma-2"
                draggable
                :key="databind.binder_name"
                @dragstart="$emit('databind_drag_start', $event, databind)">
                    {{databind.binder_name}}   
            </v-chip>
        </v-badge>
    </div>
</template>

<script>
    export default {
        props: {
            subscribed_databinds: null,
            hidden_subscribed_databinds: null,
        },
        methods: {
            isSubscribedDatabindHidden(databind_id) {
                let is_hidden = this.hidden_subscribed_databinds.findIndex(item => item == databind_id) > -1; 
                return is_hidden
            },
        }
    }
</script>