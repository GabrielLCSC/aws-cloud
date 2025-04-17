<template>
    <div class="max-w-4xl mx-auto py-10 space-y-6">
      <h1 class="text-3xl text-white font-bold text-center">Astronomy Picture of the Day</h1>
      
      <div
        v-for="item in apodData"
        :key="item.date"
        class="max-w-2xl mx-auto mt-10 space-y-6 relative z-10 p-6 text-white background-color p-12 rounded shadow space-y-3"
      >
        <h2 class="text-xl font-semibold">{{ item.title }}</h2>
        <p class="text-gray-300 text-sm">{{ item.date }}</p>
  
        <img
          v-if="item.mediaType === 'image'"
          :src="item.imageUrl"
          alt="NASA APOD"
          class="w-full rounded object-cover max-h-[600px] mx-auto"
        />
  
        <video
          v-else-if="item.mediaType === 'video'"
          controls
          class="w-full rounded"
        >
          <source :src="item.imageUrl" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
  
        <p>{{ item.description }}</p>
  
        <div class="text-right text-xs text-gray-400" v-if="item.copyright">
          &copy; {{ item.copyright }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { get } from '@aws-amplify/api-rest'
  import { message } from 'ant-design-vue'
  
  const apodData = ref([])
  
  onMounted(async () => {
    try {
      const res = await get({
        apiName: 'nasa',
        path: '/getApodData'
      })
  
      const { body } = await res.response
      const data = await body.json()
  
      apodData.value = Array.isArray(data) ? data : [data]
    } catch (error) {
      console.error('[APOD ERROR]', error)
      message.error("❌ Erreur lors du chargement des données NASA.")
    }
  })
  </script>
  
  <style scoped>
  .background-color {
    background-color: #131313;
    overflow-y: scroll;
    height: 700px;
  }
</style>
  