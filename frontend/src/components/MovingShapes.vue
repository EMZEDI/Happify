<template>
    <div class="flex-grow h-screen duration-1000 overflow-hidden bg-slate-50">
      <div class="w-full flex">
        <div
          class=" p-1 duration-1000 flex items-end justify-end"
          :style="{ width: left_x + '%', height: top_y + 'vh' }"
        >
          <div
            class="tk-blob duration-1000"
            :style="{
              width: tl * shape_scale_mult + 'vh',
              height: tl * shape_scale_mult + 'vh',
            }"
            style="--time: 60s; --amount: 5"
          >
              <svg class="fill-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 353.7 353.7">
                <path class="shadow-xl"
                  d="M291.8 55.3c30.4 39.9 30.7 102 17 160.4-13.8 58.3-41.6 112.9-84 130.9s-99.3-.6-137-30C50.2 287.1 32 246.9 17 200.5 2.1 154.1-9.6 101.4 11.5 63.6 32.6 25.8 86.6 2.8 143.8.2c57.2-2.6 117.6 15.2 148 55.1z"
                ></path>
              </svg>
          </div>
        </div>
        <div
          class=" p-1 duration-1000 flex items-end justify-begin"
          :style="{ width: right_x + '%', height: top_y + 'vh' }"
        >
          <div
            class="tk-blob duration-1000"
            :style="{
              width: tr * shape_scale_mult + 'vh',
              height: tr * shape_scale_mult + 'vh',
            }"
            style="--time: 60s; --amount: 5"
          >
            <svg class="fill-yellow-300" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 428.4 428.4">
              <path
                d="M369.4 109.2c43.2 55.3 71.5 121.4 53.4 167.3-18.2 45.8-82.8 71.4-140.5 91.7-57.8 20.4-108.7 35.4-152.9 20.3C85.1 373.4 47.6 328.3 23.2 267c-24.5-61.2-35.8-138.6-2.5-191.7C54.1 22.2 132-6.6 200 1.3c68 7.9 126.1 52.5 169.4 107.9z"
              ></path>
            </svg>
          </div>
        </div>
      </div>
      <div class="w-full flex">
        <div
          class=" duration-1000 p-1 flex items-begin justify-end"
          :style="{ width: left_x + '%', height: bottom_y + 'vh' }"
        >
          <div
            class="tk-blob duration-1000"
            :style="{
              width: bl * shape_scale_mult + 'vh',
              height: bl * shape_scale_mult + 'vh',
            }"
            style="--time: 60s; --amount: 5"
          >
            <svg class="fill-orange-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 374.7 374.7">
              <path
                d="M309.9 70.6c37.8 52.7 39.8 128.7 15.4 184.1-24.3 55.4-75 90.1-125.4 107.4-50.4 17.4-100.4 17.4-136.2-3.3-35.7-20.7-57.2-62-62.4-102.1-5.2-40.2 5.8-79 29.1-128.3C53.6 79.1 89.1 19.3 143.7 4.1 198.3-11.2 272 18 309.9 70.6z"
              ></path>
            </svg>
          </div>
        </div>
        <div
          class="duration-1000 p-1 flex items-begin justify-begin"
          :style="{ width: right_x + '%', height: bottom_y + 'vh' }"
        >
          <div
            class="tk-blob duration-1000"
            :style="{
              width: br * shape_scale_mult + 'vh',
              height: br * shape_scale_mult + 'vh',
            }"
            style="--time: 60s; --amount: 5"
          >
            <svg class="fill-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 412.3 412.3">
              <path
                d="M320.8 58.4c47.1 38.8 97.8 95 90.8 143s-71.7 87.7-138.3 117.2c-66.5 29.5-134.7 48.7-186.4 26.5C35.3 322.9.3 259.3 0 203.3-.3 147.4 34.1 99.2 71 62.8 107.9 26.3 147.2 1.7 188.7.1c41.4-1.7 84.9 19.6 132.1 58.3z"
              ></path>
            </svg>
          </div>
        </div>
      </div>
    </div>
</template>
<script setup>
import { computed, defineProps } from "vue";

const props = defineProps(["x", "y"])

const x_Scale_mult = 35;
const y_Scale_mult = 25;

const shape_scale_mult = 0.9;

const right_x = computed(() => {
  return 50 - props.x * x_Scale_mult;
});

const left_x = computed(() => {
  return 50 + props.x * x_Scale_mult;
});

const bottom_y = computed(() => {
  return 50 - props.y * y_Scale_mult;
});

const top_y = computed(() => {
  return 50 + props.y * y_Scale_mult;
});

const tl = computed(() => {
  return (top_y.value+left_x.value)/2;
});

const tr = computed(() => {
  return (top_y.value+right_x.value)/2;
});

const bl = computed(() => {
  return (bottom_y.value +left_x.value )/2;
});

const br = computed(() => {
  return (bottom_y.value + right_x.value )/2;
});
</script>