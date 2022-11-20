<template>
 
<aside class="w-64" aria-label="Sidebar">
   <div class="overflow-y-auto py-4 px-3 bg-gray-50 rounded dark:bg-gray-800" >
      <a href="https://flowbite.com/" class=" flex items-right pl-2.5 mb-5">
         
         <span class="text-4xl font-semibold whitespace-nowrap dark:text-white" >Happify</span>
      </a>
      <ul class="space-y-2">
         <li>
            <a href="#" class="flex items-center p-2 text-base font-normal fill-orange-400 rounded-lg dark:text-white hover:fill-orange-400 dark:hover:fill-orange-400">
                <div class="w-6 h-6 bg-orange-400 rounded-full"></div>
                <span class="ml-3">Sad & Productive</span>
            </a>
         </li>
         
         <li>
            <a href="#" class="flex items-center p-2 text-base font-normal fill-orange-400 rounded-lg dark:text-white hover:fill-orange-400 dark:hover:fill-orange-400">
                <div class="w-6 h-6 bg-green-500 rounded-full"></div>
                <span class="ml-3">Happy & Productive</span>
            </a>
         </li>
         
         <li>
            <a href="#" class="flex items-center p-2 text-base font-normal fill-orange-400 rounded-lg dark:text-white hover:fill-orange-400 dark:hover:fill-orange-400">
                <div class="w-6 h-6 bg-yellow-300 rounded-full"></div>
                <span class="ml-3">Happy & Distracted</span>
            </a>
         </li>
         
         <li>
            <a href="#" class="flex items-center p-2 text-base font-normal fill-orange-400 rounded-lg dark:text-white hover:fill-orange-400 dark:hover:fill-orange-400">
                <div class="w-6 h-6 bg-red-500 rounded-full"></div>
                <span class="ml-3">Sad & Distracted</span>
            </a>
         </li>

         <li>
                 <p>{{props.x.toFixed(2)}}{{props.y.toFixed(2)}}= (x,y)  </p> 
            
         </li>

        
        
      </ul>
   </div>
</aside>

  </template>
  <script setup>
  import { defineProps } from "vue";
  const props = defineProps(["x", "y"])
  
  </script>
  
  <style>
  .song{
      @apply mx-4 my-4 pb-0 bg-gray-100 rounded-lg shadow-sm
  }
  </style>