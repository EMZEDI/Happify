<template>
  <div class="w-[35vh] h-[58vh]">
    <div class="flex flex-col-reverse overflow-auto h-[58vh] z-0">
      <div v-if="props.previouslyplayed">
        <div
          class="song"
          v-bind:key="item.item.id"
          v-for="item in props.previouslyplayed"
        >
          <div class="flex">
            <img class="w-20 h-20" :src="item.item.album.images[0].url" />
            <div class="h-20 pt-4 ml-4">
              <p class="text-lg">{{ item.item.name.substring(0, 21) }}</p>
              <p class="text-sm">{{ item.item.artists[0].name }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div style="box-shadow: 0 0 15px rgb(0 0 0/.1)" class="w-[35vh] h-[42vh] z-30 flex items-center justify-center">
    <div v-if="props.song">
    <div class="w-[35vh] h-[35vh] pb-2 flex items-center justify-center">  
        <div>
        <img class="mt-4 w-[30vh] h-[30vh] shadow-md rounded-lg" :src="props.song.item.album.images[0].url" />
        <div class="mt-2">
            <p class="text-xl">{{ props.song.item.name.substring(0, 25) }}</p>
        <p class="text-lg">{{ props.song.item.artists[0].name }}</p>
        </div>
    </div>
    </div>  
    </div>
  </div>
</template>
<script setup>
import { defineProps } from "vue";

const props = defineProps(["song", "previouslyplayed"])

</script>

<style>
.song{
    @apply mx-4 my-4 pb-0 bg-slate-100 rounded-lg shadow-sm
}
</style>