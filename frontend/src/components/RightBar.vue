<template>
  <div>
    <div class="overflow-y-auto p-8">
      <div class="mb-4 text-4xl text-right font-semibold whitespace-nowrap">
        Happify
      </div>
      <div class="space-y-4 text-right">
        <div class="text-lg">Color Key</div>
        <div class="text-gray-500 space-y-4">

          <div class="flex float-right">
            <span class="mr-3">Happy & Productive</span>
            <div class="w-6 h-6 bg-green-500 rounded-full"></div>
          </div>

          <div class="flex float-right">
            <span class="mr-3">Happy & Distracted</span>
            <div class="w-6 h-6 bg-yellow-300 rounded-full"></div>
          </div>

          <div class="flex float-right">
            <span class="mr-3">Sad & Productive</span>
            <div class="w-6 h-6 bg-orange-400 rounded-full"></div>
          </div>

          <div class="flex float-right">
            <span class="mr-3">Sad & Distracted</span>
            <div class="w-6 h-6 bg-red-500 rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="absolute bottom-0 right-0 w-[35vh] h-[24vh] text-center">
      <p>Current Sentiment:</p>
      <div class="flex items-center justify-center py-4">
      <div class="relative w-[10vh] h-[10vh]">
        <div class="flex absolute top-0 left-0 w-[10vh] h-[10vh] rounded-lg overflow-hidden">
          <div class="w-full">
          <div class="w-[5vh] h-[5vh] bg-green-500/50">
          </div>
          <div class="w-[5vh] h-[5vh] bg-orange-400/50">
          </div>
          </div>
          <div class="w-full">
          <div class="w-[5vh] h-[5vh] bg-yellow-300/50">
          </div>
          <div class="w-[5vh] h-[5vh] bg-red-500/50">
          </div>
          </div>
        </div>
        <!-- <div class="absolute top-0 left-[1px] w-[5vh] h-full border-r-2 border-indigo-500"></div>
        <div class="absolute top-[1px] left-0 h-[5vh] w-full border-b-2 border-indigo-500"></div> -->
        <div class="w-4 h-4 absolute bg-indigo-700 rounded-full z-20" :style="{ bottom: (4+props.y*5) + 'vh', right: (4+props.x*5) + 'vh' }">
        </div>
      </div>
      </div>
      <p>{{ props.x.toFixed(2) }}, {{ props.y.toFixed(2) }} = (x,y)</p>
    </div>
  </div>
</template>
<script setup>
import { defineProps } from "vue";
const props = defineProps(["x", "y"]);
</script>

<style>
.song {
  @apply mx-4 my-4 pb-0 bg-gray-100 rounded-lg shadow-sm;
}
</style>
