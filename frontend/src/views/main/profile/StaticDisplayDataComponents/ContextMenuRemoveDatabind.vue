<template>
    <v-menu
        v-bind:value="show"
        :position-x=position_x
        :position-y=position_y
        absolute
        offset-y>

        <v-list>
            <v-list-item
            @click="$emit('removeDatabindClicked')">
                <v-list-item-title>Remove databind...</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</template>

<script>
    export default {
        props: {
            position_x: 0,
            position_y: 0,
            show: null
        }
    }
</script>

