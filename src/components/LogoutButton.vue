<!-- src/components/LogoutButton.vue -->
<template>
    <a-button type="default" danger block @click="handleLogout" :loading="loading">
      <template #icon>
        <i class="ri-logout-box-r-line" />
      </template>
      Se déconnecter
    </a-button>
  </template>
  
  <script setup>
  import { signOut } from '@aws-amplify/auth'
  import { useRouter } from 'vue-router'
  import { message } from 'ant-design-vue'
  import { ref } from 'vue'
  
  const router = useRouter()
  const loading = ref(false)
  
  async function handleLogout() {
    loading.value = true
    try {
      await signOut()
      message.success('👋 À bientôt !')
      router.push('/login')
    } catch (err) {
      console.error('[LOGOUT ERROR]', err)
      message.error('❌ Erreur lors de la déconnexion.')
    } finally {
      loading.value = false
    }
  }
  </script>
  