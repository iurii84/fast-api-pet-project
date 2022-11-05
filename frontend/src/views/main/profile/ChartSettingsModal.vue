<template>
       
    <div>
        <b-modal :static="true" id="temp-hum-settings-modal" title="chart settings" >
        <p class="my-4">Settings
            <div>
                Load interval: {{load_interval}}
            </div>
            <br>
            <div> 
                <b-form-select  id="select_update_time_interval" v-model="update_chart_after" :options="update_chart_interval_options"></b-form-select>
            </div>
        </p>
        
        </b-modal>
    </div>
    
</template>

<script lang="ts">
import { Component, Vue, Prop, Emit, Watch } from 'vue-property-decorator';


@Component
export default class ChartSettingsModal extends Vue {
    // @Prop({default: 0}) public load_interval: number;

    public data() {
        return {
            load_interval: null,
            update_chart_after: null,
            update_chart_interval_options: [
                { value: 1, text: 'Every second' },
                { value: 3, text: 'Each 3 seconds' },
                { value: 5, text: 'Each 5 seconds' },
                { value: 10, text: 'Each 10 seconds' },
                { value: 15, text: 'Each 15 seconds'},
            ],
        };
    }
    public mounted() {
        if (localStorage.update_chart_after) {
                // this.update_chart_after = localStorage.update_chart_after;
            }
    }

    @Watch('update_chart_after')
    public onUpdateChartAfterValueChanged(update_chart_after_value) {
        localStorage.update_chart_after = update_chart_after_value;
        this.$emit('on-update-chart-after-value-changed', update_chart_after_value);
    }



}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#select_update_time_interval {
    outline: auto;
    outline-width: 2px;
    padding: 5px;
}

</style>