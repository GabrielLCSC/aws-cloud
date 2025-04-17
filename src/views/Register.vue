<template>
  <div class="relative z-10 min-vh-100 d-flex align-items-center justify-content-center">
    <div class="w-100 px-3" style="max-width: 500px">
      <div class="background-color p-4 rounded shadow">
        <div class="flex items-center justify-center gap-2 text-white mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 stroke-current" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4m-4-4l4-4m0 0l-4-4m4 4H3" />
        </svg>
        <h2 class="text-xl font-semibold">Créer un compte</h2>
      </div>

        <a-form @submit.prevent="handleSubmit" layout="vertical">
          <InputForm v-model="form.email" type="email" text="Email" />
          <InputForm v-model="form.lastName" type="text" text="Nom" />
          <InputForm v-model="form.firstName" type="text" text="Prénom" />
          <InputForm v-model="form.password" type="password" text="Mot de passe" />
          <InputForm v-model="form.confirmPassword" type="password" text="Confirmer le mot de passe" />
          <LoginButton type="primary"
            html-type="submit" text="Créer un compte" class="mt-4" :loading="loading" />
        </a-form>

        <p class="text-white mt-3 text-center">
          Déjà un compte ?
          <router-link to="/login" class="text-primary text-decoration-none ms-1">
            Connecte-toi
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { signUp } from '@aws-amplify/auth'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import InputForm from '@/components/InputForm.vue'
import LoginButton from '@/components/LoginButton.vue'

const router = useRouter()

const form = reactive({
  email: '',
  firstName: '',
  lastName: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)

async function handleSubmit() {
  if (form.password !== form.confirmPassword) {
    message.error("Les mots de passe ne correspondent pas.")
    return
  }

  loading.value = true

  try {
    
    await signUp({
      username: form.email,
      password: form.password,
      options: {
        userAttributes: {
          email: form.email,
          name: form.firstName,
          family_name: form.lastName
        },
      }
    })

    
    message.success('🎉 Compte créé avec succès ! Redirection…')
    router.push({ path: '/confirm', query: { email: form.email } })
  } catch (err) {
    console.error('[SIGNUP ERROR]', err)

    if (err.name === 'InvalidPasswordException') {
      message.error("🔒 Mot de passe trop faible : 8 caractères minimum.")
    } else if (err.name === 'UsernameExistsException') {
      message.warning("🚨 Un compte avec cet email existe déjà.")
    } else if (err.name === 'InvalidParameterException') {
      message.error("⚠️ Paramètres invalides (ex: email mal formé).")
    } else {
      message.error(err.message || '❌ Erreur inconnue')
    }
  } finally {
    loading.value = false
  }
}
</script>
<style scoped>
  .background-color {
    background-color: #131313;
  }
</style>