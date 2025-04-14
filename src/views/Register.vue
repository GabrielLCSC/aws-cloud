<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="w-100 px-3" style="max-width: 500px">
      <div class="bg-white p-4 rounded shadow">
        <h2 class="text-center mb-4">Créer un compte</h2>

        <a-form @submit.prevent="handleSubmit" layout="vertical">
          <a-form-item label="Email">
            <a-input v-model:value="form.email" type="email" required />
          </a-form-item>

          <a-form-item label="Nom">
            <a-input v-model:value="form.lastName" type="text" required />
          </a-form-item>

          <a-form-item label="Prénom">
            <a-input v-model:value="form.firstName" type="text" required />
          </a-form-item>

          <a-form-item label="Mot de passe">
            <a-input-password v-model:value="form.password" required />
          </a-form-item>

          <a-form-item label="Confirmer le mot de passe">
            <a-input-password v-model:value="form.confirmPassword" required />
          </a-form-item>

          <a-button
            type="primary"
            html-type="submit"
            class="w-100"
            :loading="loading"
          >
            Créer un compte
          </a-button>
        </a-form>

        <p class="mt-3 text-center">
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
import {post} from '@aws-amplify/api-rest'
import { message } from 'ant-design-vue'


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
    const restOperation = post('users', '/insertUser', {
      body: {
        email: form.email,
        firstName: form.firstName,
        lastName: form.lastName,
        password: form.password
      }
    })

    const { body } = await restOperation.response;
    const response = await body.json();

    message.success('🎉 Compte créé avec succès ! Redirection…')
    console.log('✔️ Réponse backend :', response)

  } catch (err) {
    const status = err?.response?.status
    if (status === 409) {
      message.warning("🚨 Un compte avec cet email existe déjà.")
    } else {
      message.error("❌ Erreur serveur, réessayez plus tard.")
    }
    console.error('❌ Erreur :', err)
  } finally {
    loading.value = false
  }
}
</script>
