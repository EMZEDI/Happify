<template>
  <div class="w-full h-screen">
    <div class="w-[30vh] h-screen">
      <div class="w-[30vh] h-[70vh] overflow-hidden">
        <div class="overflow-hidden min-h-0" v-if="previouslyplayed">
          <div
            v-bind:key="item.track.id"
            v-for="item in previouslyplayed.items.reverse()"
          >
            <div>
              <img :src="item.track.album.images[0].url"/>
              {{ item.track.name }}
              {{ item.track.artist }}
            </div>
          </div>
        </div>
      </div>
      <div class="w-[30vh] h-[30vh] bg-black"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const ws = ref(null);
const song = ref(null);

const previouslyplayed = ref(null);

onMounted(() => {
  axios
    .get("http://127.0.0.1:3000/previoussongs")
    .then((response) => (previouslyplayed.value = response.data));
  ws.value = new WebSocket("ws://127.0.0.1:3000/streamtrack");
  ws.value.onmessage = function (event) {
    song.value = event.data;
  };
});
</script>
