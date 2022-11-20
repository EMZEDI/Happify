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
            <span class="mr-3">Sad & Productive</span>
            <div class="w-6 h-6 bg-orange-400 rounded-full"></div>
          </div>

          <div class="flex float-right">
            <span class="mr-3">Happy & Productive</span>
            <div class="w-6 h-6 bg-green-500 rounded-full"></div>
          </div>

          <div class="flex float-right">
            <span class="mr-3">Happy & Distracted</span>
            <div class="w-6 h-6 bg-yellow-300 rounded-full"></div>
          </div>

          <div class="flex float-right">
            <span class="mr-3">Sad & Distracted</span>
            <div class="w-6 h-6 bg-red-500 rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="absolute bottom-0 right-0 w-[35vh] h-[10vh] text-center">
      <p>Current Sentiment:</p>
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
