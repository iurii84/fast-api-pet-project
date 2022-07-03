<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Temperature and humidity data</div>
      </v-card-title>
      <div class="temp-hum-chart" ref="chartdiv"></div> 
      <br>
      <div class="time-interval-selector">   
        Select time interval: 
      <v-select
          @input="when_time_interval_changed" 
          v-model="selected"
          :reduce="(option) => option.id"
          :options="[
            { label: '1H', id: 1 * 60 },
            { label: '4H', id: 4 * 60},
            { label: '12H', id: 12 * 60},
            { label: '24H', id: 24 * 60},
    
          ]"
          :clearable=false
      />
      </div>
      <br>
      <span> 
        {{ selected/60 }} hours interval selected
      </span>

    </v-card>
  </v-container>
</template>

<script>

import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

import Vue from 'vue'
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';
Vue.component('v-select', vSelect);
am4core.useTheme(am4themes_animated);




export default { 
  name: 'temp-hum', 

  methods: {
    when_time_interval_changed(){
      //reload data for incremental type chart doesn't work. Need to create another chart entity

      //dispose old chart entity
      if (this.chart) {
        this.chart.dispose();
      }
   
      let chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
      chart.dateFormatter.timezoneOffset = 480;
      chart.paddingRight = 20;
      let data = [];
  
    
      //create the new one
      chart.dataSource.url = "http://192.168.88.254/api/v1/message?lastMinutes=" + this.selected,
      chart.dataSource.incremental = true;
      chart.dataSource.reloadFrequency = 5000;
      chart.dataSource.keepCount = true;
      //try-catch if missed data. Prevent accessing empty array by id
      chart.dataSource.adapter.add("incrementalParams", function(params, target) {
          try{
            params.after_id = target.data[target.data.length - 1]['id'];
            }
          catch(error) {
            }
          
          return params;
        }
      );

      

      let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
      dateAxis.renderer.grid.template.location = 0;

      let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
      valueAxis.tooltip.disabled = false;
      valueAxis.renderer.minWidth = 35;

      let series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = "created";
      series.dataFields.valueY = "hum";

      let series_temp = chart.series.push(new am4charts.LineSeries());
      series_temp.stroke = am4core.color("#ff0000"); // red
      series_temp.dataFields.dateX = "created";
      series_temp.dataFields.valueY = "temp";

      series.tooltipText = "{valueY.hum}";
      series_temp.tooltipText = "{valueY.temp}";
      chart.cursor = new am4charts.XYCursor();

      let scrollbarX = new am4charts.XYChartScrollbar();
      scrollbarX.series.push(series);
      chart.scrollbarX = scrollbarX;

      this.chart = chart;
      //ISO date-time format data from DB
      chart.dateFormatter.inputDateFormat = "i";
      

    }
  },
  

  

  data() {
    return {
      selected: 60
    }
  },
  
  mounted() {
    //call for initial data
    this.when_time_interval_changed();
   },

  

  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
    }
  }
}



</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.temp-hum-chart {
  width: 100%;
  height: 500px;
}

.time-interval-selector {
  width: 10%;
}

</style>