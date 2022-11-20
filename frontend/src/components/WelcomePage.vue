<template>
  <div className="w-screen h-screen flex justify-center items-center">
    <div>
      <div className="text-4xl text-center mb-4 font-bold">Happify</div>
      <div
        className="w-96 mt-6 p-12 text-gray-700 text-left transition-all rounded-2xl shadow-xl"
      >
        <p>Happify intends to keep you always in the zone, remixing playlists of your choice gradually according to your current state of mind. </p>

        <p class="mt-2">We use machine learning and vision to calculate your current state then use an algorithm to queue the best song as we transition you to the best playlist for your current state of mind.</p>

        <p class="mt-2">We provide a digital dashboard to watch the live status of your Spotify state, emotional state, and upcoming songs as the machine learning model proposes new songs.</p>

        <div class="pt-6 text-right">
        <span @click="router.push('/setup')" class="hover:bg-blue-400 bg-blue-600 cursor-pointer  p-4 rounded-full px-8 text-white">Setup</span>
    </div>
    </div>
      <!-- <a href="https://github.com/tvut/forest"
        ><FontAwesomeIcon icon="{faGithub}"
      /></a> -->
      <p className="text-center text-gray-600 mt-4 text-sm">
        Codejam 2022.
      </p>
    </div>
  </div>
</template>
<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>
