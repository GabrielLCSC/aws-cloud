<!-- src/components/LogoutButton.vue -->
<template>
    <button class="relative w-fit h-[40px] bg-black text-white flex items-center justify-center flex-col gap-3 p-3 rounded-lg cursor-pointer before:content-[''] before:absolute before:-left-1 before:-top-0.5 before:w-[155px] before:h-[48px] before:rounded-[10px] before:bg-gradient-to-br before:from-[#e81cff] before:to-[#40c9ff] before:-z-10 before:pointer-events-none before:transition-all before:duration-[600ms] before:ease-[cubic-bezier(0.175,0.885,0.32,1.275)] after:content-[''] after:absolute after:inset-0 after:-z-[1] after:bg-gradient-to-br after:from-[#fc00ff] after:to-[#00dbde] after:scale-[0.95] after:blur-[20px] hover:after:blur-[30px] hover:before:rotate-[-180deg] active:before:scale-75" type="default" @click="handleLogout" :loading="loading">
      Se déconnecter
    </button>
  </template>
  
  <script setup>
  import '@/assets/tailwind.css'
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
  