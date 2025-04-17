<template>
    <div class="max-w-4xl mx-auto py-10 space-y-6">
      <h1 class="text-3xl text-white font-bold text-center">Astronomy Picture of the Day</h1>
  
      <div
        :key="testmock.date"
        class="max-w-2xl mx-auto mt-10 space-y-6 relative z-10 p-6 text-white background-color p-12 rounded shadow space-y-3"
      >
        <h2 class="text-xl font-semibold">{{ testmock.title }}</h2>
        <p class="text-gray-300 text-sm">{{ testmock.date }}</p>
  
        <img
          v-if="testmock.mediaType === 'image'"
          :src="testmock.imageUrl"
          alt="NASA APOD"
          class="w-full rounded object-cover max-h-[600px] mx-auto"
        />
  
        <video
          v-else-if="testmock.mediaType === 'video'"
          controls
          class="w-full rounded"
        >
          <source :src="testmock.imageUrl" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
  
        <p>{{ testmock.description }}</p>
  
        <div class="text-right text-xs text-gray-400" v-if="testmock.copyright">
          &copy; {{ testmock.copyright }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { get } from '@aws-amplify/api-rest'
  import { message } from 'ant-design-vue'

  const testmock = {
    date: new Date().toLocaleDateString(),
    title: 'title',
    mediaType: 'image',
    imageUrl: 'https://picsum.photos/600/600',
    description: 'Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.',
    copyright: 'copyright',
  }
  
  const apodData = ref([])
  
  onMounted(async () => {
    try {
      const res = await get({
        apiName: 'nasa',
        path: '/getApodData'
      })
  
      const { body } = await res.response
      const data = await body.json()

      console.log({data})
  
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
  