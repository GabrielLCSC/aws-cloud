<template>
    <div class="space-y-4">
      <a-upload
        :customRequest="handleUpload"
        :showUploadList="false"
        accept="image/*"
      >
        <a-button type="dashed" block>
          📸 Ajouter une photo de profil
        </a-button>
      </a-upload>
  
      <div v-if="imageUrl">
        <p class="mb-1">Aperçu :</p>
        <img :src="imageUrl" class="rounded shadow" style="max-width: 200px" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { Storage } from '@aws-amplify/storage'
  import { getCurrentUser } from 'aws-amplify/auth'
  
  const imageUrl = ref(null)
  
  async function handleUpload({ file, onSuccess, onError }) {
    try {
      const { username } = await getCurrentUser()
      const filename = `avatars/${username}_${Date.now()}_${file.name}`
  
      await Storage.put(filename, file, {
        contentType: file.type,
      })
  
      const url = await Storage.get(filename)
      imageUrl.value = url
      onSuccess(null, file)
    } catch (error) {
      console.error('[Upload ERROR]', error)
      onError(error)
    }
  }
  </script>
  