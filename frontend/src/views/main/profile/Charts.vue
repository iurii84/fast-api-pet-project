<template>
  <v-card class="ma-5 pa-5">
    <v-card-title primary-title>
      <div class="headline primary--text">Temperature and humidity data</div>
    </v-card-title>
    <ChartSettingsModal :load_interval=this.selected 
                        @on-update-chart-after-value-changed="callback_chart_after_value_changed" />
    
    <div></div>
    <div class="temp-hum-data-avg-now">
      <span class="temp-data-avg-now">
        Temperature: {{temp}}
      </span>
      <span class="hum-data-avg-now">
        Humidity: {{hum}}
      </span>
      <span id="chart-settings-button">
        <b-button v-b-modal.temp-hum-settings-modal variant="outline-secondary">Chart settings</b-button>
      </span>
    </div>
    <div class="temp-hum-chart" ref="chartdiv"></div> 
    <br>
    <div class="time-interval-selector">   
      Select time interval: 
      <v-select
          @input="when_time_interval_changed" 
          v-model="selected"
          dense
          :items="[
            { text: '15m', value: 15 },
            { text: '1H', value: 1 * 60 },
            { text: '4H', value: 4 * 60},
            { text: '12H', value: 12 * 60},
            { text: '24H', value: 24 * 60},
            { text: '3d', value: 24 * 60 * 3},
            { text: '1w', value: 24 * 60 * 7},
          ]"
      />
    </div>
    <br>
    <span> 
      {{ selected/60 }} hours interval selected
    </span>

  </v-card>
</template>

<script>
import ChartSettingsModal from './ChartSettingsModal.vue';
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

import Vue from 'vue'

am4core.useTheme(am4themes_animated);




export default { 
  name: 'temp-hum', 

  components:{
    ChartSettingsModal
  },

  methods: {
    callback_chart_after_value_changed(value){
      this.chart_after_value = value * 1000;
      this.when_time_interval_changed();
    },
    
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
      chart.dataSource.reloadFrequency = this.chart_after_value;
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
      series.name = "humidity";
      

      let series_temp = chart.series.push(new am4charts.LineSeries());
      series_temp.stroke = am4core.color("#ff0000"); // red
      series_temp.dataFields.dateX = "created";
      series_temp.dataFields.valueY = "temp";
      series_temp.name = "temperature";

      series.tooltipText = "{valueY.hum}";
      series_temp.tooltipText = "{valueY.temp}";
      chart.cursor = new am4charts.XYCursor();

      let scrollbarX = new am4charts.XYChartScrollbar();
      scrollbarX.series.push(series);
      chart.scrollbarX = scrollbarX;

      chart.legend = new am4charts.Legend();
      

      this.chart = chart;
      //ISO date-time format data from DB
      //"this" indicate the context! So it should be here!
      chart.dateFormatter.inputDateFormat = "i";
      
      chart.dataSource.events.on("loadended", function() {
        let dataset = chart._data;
        let len_dataset = dataset.length;
        let buf_temp = 0;
        let buf_hum = 0;
        if (len_dataset>0) {
          for (let i=0; i < 10; i++){
            let data_msg = dataset[len_dataset-1-i];
            buf_temp += data_msg['temp'];
            buf_hum += data_msg['hum'];
          }
          self.temp = Math.round((buf_temp/10 + Number.EPSILON) * 10) / 10;
          self.hum =  Math.round((buf_hum/10 + Number.EPSILON) * 10) / 10;
          console.log(self.temp);
          
          this.hum = self.hum;
          this.temp = self.temp;
        }
        
       
      }, this); 

      
     

    }
  },
  
 
  

  data() {
    return {
      selected: 60,
      temp: 0,
      hum: 0,
      chart_after_value: 5000
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

.temp-hum-data-avg-now {
  font-size: 22px;
  margin-left: 15px;
}

.temp-data-avg-now {
  color: red;
}

.hum-data-avg-now {
  margin-left: 20px;
  color: blue;
}

#chart-settings-button {
  float: right;
}

</style>