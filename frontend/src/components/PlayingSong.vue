<template>
  <div class="w-[35vh]" :class="(props.upnext)?'h-[46vh]':'h-[58vh]'">
    <!-- <div class="absolute top-0 left-0 w-[35vh] bg-white p-4 shadow-lg">
        <p1 class="text-xl">Recently Played</p1>
    </div> -->
    <div class="pb-1 flex flex-col-reverse overflow-auto z-0" :class="(props.upnext)?'h-[46vh]':'h-[58vh]'">
      <div v-if="props.previouslyplayed">
        <div class="song" v-bind:key="item.item.id" v-for="item in props.previouslyplayed">
          <div class="flex">
            <img class="rounded-l-lg w-20 h-20" :src="item.item.album.images[0].url" />
            <div class="h-20 pt-4 ml-4">
              <p class="text-lg">{{ item.item.name.split('(')[0].substring(0, 15) }}</p>
              <p class="text-sm">{{ item.item.artists[0].name }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div :class="(props.upnext)?'h-[54vh]':'h-[42vh]'" style="box-shadow: 0 0 15px rgb(0 0 0/.1)" class="w-[35vh] z-30 flex items-center justify-center">
    <div>
    <div v-if="props.song">
      <div class="w-[35vh] h-[35vh] pb-2 flex items-center justify-center">
        <div>
          <img class="mt-4 w-[30vh] h-[30vh] shadow-md rounded-lg" :src="props.song.item.album.images[0].url" />
          <div class="mt-2">
            <p class="text-xl">{{ props.song.item.name.substring(0, 23) }}</p>
            <p class="text-lg">{{ props.song.item.artists[0].name }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="pt-3" v-if="props.upnext">
      <div class="song">
          <div class="flex">
            <img class="rounded-l-lg w-24 h-24" :src="props.upnext.album.images[0].url" />
            <div class="h-24 pt-2 ml-4">
              <p class="text-md text-indigo-700">Up next:</p>
              <p class="text-lg">{{ props.upnext.name.split('(')[0].substring(0, 15) }}</p>
              <p class="text-sm">{{ props.upnext.artists[0].name }}</p>
            </div>
          </div>
        </div>
    </div>
  </div>
  </div>
</template>
<script setup>
import { defineProps } from "vue";

const props = defineProps(["song", "previouslyplayed", "upnext"])

</script>

<style>
.song {
  @apply mx-4 my-4 pb-0 bg-gray-100 rounded-lg shadow-sm
}
</style>