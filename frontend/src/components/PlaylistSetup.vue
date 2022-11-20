<template>
  <div class="w-full h-screen flex overflow-hidden">
    <div class="w-1/3">
      <p class="m-4 my-6 text-3xl font-bold">Select Your Playlists</p>
      <div class="overflow-scroll h-full pb-24" v-if="playlists">
        <draggable
          class="-mt-4"
          v-model="playlists"
          group="people"
          @start="drag = true"
          @end="drag = false"
          item-key="id"
        >
          <template #item="{ element }">
            <div class="m-4 bg-gray-100 rounded-lg shadow-sm cursor-pointer">
              <div class="flex">
                <div v-if="element.images[0]">
                  <img
                    class="rounded-l-lg w-20 h-20"
                    :src="element.images[0].url"
                  />
                </div>
                <div class="h-20 pt-4 ml-4">
                  <p class="text-lg">
                    {{ element.name }}
                  </p>
                  <p class="text-sm">{{ element.owner.display_name }}</p>
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>
    </div>
    <div class="flex-grow">
      <div class="flex w-full">
        <div class="w-1/2 h-[50vh] relative">
          <div class="absolute top-0 left-0 w-full h-full flex items-center justify-center">
            <p class="text-2xl">Chill Favorites</p>
          </div>
          <draggable
            class="w-full h-[50vh] sqr bg-green-300"
            v-model="happy_prod"
            group="people"
            @start="drag = true"
            @end="drag = false"
            item-key="id"
          >
            <template #item="{ element }">
              <div
                :style="{
                  'background-image': 'url(' + element.images[0].url + ')',
                }"
                class="bg-cover w-full h-[50vh] flex items-center justify-center"
              >
                <div
                  class="bg-black/20 h-full w-full flex items-center justify-center"
                >
                  <div
                    class="backdrop-blur-md p-10 h-full w-full flex items-center justify-center"
                  >
                    <p class="text-3xl text-center text-white">{{ element.name }}</p>
                  </div>
                </div>
              </div>
            </template>
          </draggable>
        </div>
        <div class="w-1/2 h-[50vh] relative">
          <div class="absolute top-0 left-0 w-full h-full flex items-center justify-center">
            <p class="text-2xl">Chill Working Music</p>
          </div>
          <draggable
            class="w-full h-[50vh] sqr bg-yellow-300"
            v-model="happy_unprod"
            group="people"
            @start="drag = true"
            @end="drag = false"
            item-key="id"
          >
            <template #item="{ element }">
              <div
                :style="{
                  'background-image': 'url(' + element.images[0].url + ')',
                }"
                class="bg-cover w-full h-[50vh] flex items-center justify-center"
              >
                <div
                  class="bg-black/20 h-full w-full flex items-center justify-center"
                >
                  <div
                    class="backdrop-blur-md p-10 h-full w-full flex items-center justify-center"
                  >
                    <p class="text-3xl text-center text-white">{{ element.name }}</p>
                  </div>
                </div>
              </div>
            </template>
          </draggable>
        </div>
      </div>
      <div class="flex w-full">
        <div class="w-1/2 h-[50vh] relative">
          <div class="absolute top-0 left-0 w-full h-full flex items-center justify-center">
            <p class="text-2xl">Favorites</p>
          </div>
          <draggable
            class="w-full h-[50vh] sqr bg-orange-400"
            v-model="sad_prod"
            group="people"
            @start="drag = true"
            @end="drag = false"
            item-key="id"
          >
            <template #item="{ element }">
              <div
                :style="{
                  'background-image': 'url(' + element.images[0].url + ')',
                }"
                class="bg-cover w-full h-[50vh] flex items-center justify-center"
              >
                <div
                  class="bg-black/20 h-full w-full flex items-center justify-center"
                >
                  <div
                    class="backdrop-blur-md p-10 h-full w-full flex items-center justify-center"
                  >
                    <p class="text-3xl text-center text-white">{{ element.name }}</p>
                  </div>
                </div>
              </div>
            </template>
          </draggable>
        </div>
        <div class="w-1/2 h-[50vh] relative">
          <div class="absolute top-0 left-0 w-full h-full flex items-center justify-center">
            <p class="text-2xl">Upbeat Working Music</p>
          </div>
          <draggable
            class="w-full h-[50vh] sqr bg-red-400"
            v-model="sad_unprod"
            group="people"
            @start="drag = true"
            @end="drag = false"
            item-key="id"
          >
            <template #item="{ element }">
              <div
                :style="{
                  'background-image': 'url(' + element.images[0].url + ')',
                }"
                class="bg-cover w-full h-[50vh] flex items-center justify-center"
              >
                <div
                  class="bg-black/20 h-full w-full flex items-center justify-center"
                >
                  <div
                    class="backdrop-blur-md p-10 h-full w-full flex items-center justify-center"
                  >
                    <p class="text-3xl text-center text-white">{{ element.name }}</p>
                  </div>
                </div>
              </div>
            </template>
          </draggable>
        </div>
      </div>
    </div>
    <div :class="(condition)?'w-1/5':'w-0'" class="flex items-center justify-center h-screen hover:bg-green-300 cursor-pointer" @click="submitPlaylists">
      <div class="text-xl">
        Continue &rarr;
      </div>
    </div>
  </div>
</template>
<script setup>
import draggable from "vuedraggable";
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const playlists = ref(null);

const happy_prod = ref([]);
const happy_unprod = ref([]);
const sad_prod = ref([]);
const sad_unprod = ref([]);

const condition = computed(() =>{
  return happy_prod.value.length == 1 && happy_unprod.value.length == 1 && sad_prod.value.length == 1 && sad_unprod.value.length == 1;
})

onMounted(() => {
  axios.get("http://127.0.0.1:3000/playlists").then((response) => {
    playlists.value = response.data.items;
    console.log(response.data.items);
  });
});

const submitPlaylists = (() => {
  axios.post('http://127.0.0.1:3000/submit-playlists', {
    happy_prod: happy_prod.value[0],
    happy_unprod: happy_unprod.value[0],
    sad_prod: sad_prod.value[0],
    sad_unprod: sad_unprod.value[0]
  })
  .then(function (response) {
    console.log(response);
    router.push('/dashboard')
  })
  .catch(function (error) {
    console.log(error);
  });
})
</script>
<style>
/* .sqr {
    @apply bg-black;
} */
</style>
