<template>
  <div class="w-full h-screen flex">
    <div class="sidebar">
      <PlayingSong :upnext="upnext" :song="song" :previouslyplayed="previouslyplayed"/>
    </div>
    <MovingShapes :x="xAxisAvg" :y="yAxisAvg" />
    <div class="sidebar absolute right-0 top-0">
      <RightBar :x="xAxis" :y="yAxis"/>
    </div>
  </div>
</template>

<script setup>
import MovingShapes from './MovingShapes.vue'
import PlayingSong from './PlayingSong.vue'
import RightBar from './RightBar.vue'
import { ref, onMounted } from "vue";
// import axios from "axios";

const ws = ref(null);

const mlws = ref(null);

const song = ref(null);

const upnext = ref(null)

const previouslyplayed = ref(null);

const xAxis = ref(-0.5);
const yAxis = ref(0.5);

const yAxisAvg = ref(0.5);
const xAxisAvg = ref(-0.5);

onMounted(() => {
  // axios.get("http://127.0.0.1:3000/previoussongs").then((response) => {
  //   previouslyplayed.value = response.data;
  // });
  mlws.value = new WebSocket("ws://127.0.0.1:3000/mlresult");
  ws.value = new WebSocket("ws://127.0.0.1:3000/streamtrack");
  ws.value.onmessage = function (event) {
    let blob = JSON.parse(event.data);
    if (blob.played != null) {
      previouslyplayed.value = JSON.parse(blob.played);
    } else if (blob.song != null) {
      song.value = blob.song;
      console.log("new song");
    } else if(blob.upnext != null){
      upnext.value = blob.upnext
      console.log(blob.upnext)
    }
  };
  mlws.value.onmessage = function (event) {
    let blob = JSON.parse(event.data);
    xAxis.value = blob.x;
    yAxis.value = blob.y;
    xAxisAvg.value = blob.avgx;
    yAxisAvg.value = blob.avgy;
  };
});
</script>
