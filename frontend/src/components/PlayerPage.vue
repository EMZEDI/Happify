<template>
  <div class="w-full h-screen flex">
    <div class="w-[40vh] h-screen">
      <div class="w-[40vh] h-[60vh]">
        <div class="flex flex-col-reverse overflow-auto h-[60vh]">
          <div v-if="previouslyplayed">
            <div
              class="mt-2"
              v-bind:key="item.item.id"
              v-for="item in previouslyplayed"
            >
              <div class="flex">
                <img class="w-16 h-16" :src="item.item.album.images[0].url" />
                <div class="h-16 pt-2 ml-4">
                  <p class="text-lg">{{ item.item.name.substring(0,30) }}</p>
                  <p class="text-sm">{{ item.item.artists[0].name }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="w-[40vh] h-[40vh] flex items-center justify-left h-screen">
        <div v-if="song" class="text-left ml-2">
          <img class="w-[30vh] h-[30vh]" :src="song.item.album.images[0].url" />
          <p class="text-xl">{{ song.item.name.substring(0, 25) }}</p>
          <p class="text-lg">{{ song.item.artists[0].name }}</p>
        </div>
      </div>
    </div>
    <div class="w-full bg-black h-screen">
      t
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
// import axios from "axios";

const ws = ref(null);
const song = ref(null);

const previouslyplayed = ref(null);

onMounted(() => {
  // axios.get("http://127.0.0.1:3000/previoussongs").then((response) => {
  //   previouslyplayed.value = response.data;
  // });
  ws.value = new WebSocket("ws://127.0.0.1:3000/streamtrack");
  ws.value.onmessage = function (event) {
    let blob = JSON.parse(event.data);
    if (blob.played != null) {
      console.log("new played list");
      console.log(JSON.parse(blob.played)[0]);
      previouslyplayed.value = JSON.parse(blob.played);
    } else if (blob.song != null) {
      song.value = blob.song;
      console.log("new song");
    }
    // song.value = JSON.parse(event.data)
    // console.log(JSON.parse(event.data))
  };
});
</script>
