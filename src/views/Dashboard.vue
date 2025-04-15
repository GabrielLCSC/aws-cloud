<template>
  <div class="max-w-2xl mx-auto mt-10 space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-semibold">Mon Profil</h2>
      <LogoutButton />
    </div>

    <!-- Formulaire -->
    <a-form layout="vertical">
      <a-form-item label="Prénom">
        <a-input v-model:value="user.firstName" />
      </a-form-item>

      <a-form-item label="Nom">
        <a-input v-model:value="user.lastName" />
      </a-form-item>

      <a-form-item label="Email">
        <a-input v-model:value="user.email" type="email" />
      </a-form-item>

      <a-divider>Informations supplémentaires</a-divider>

      <a-form-item label="Date de naissance">
        <a-date-picker
          v-model:value="user.birthDate"
          format="DD/MM/YYYY"
          style="width: 100%"
        />
      </a-form-item>

      <a-form-item label="Genre">
        <a-radio-group v-model:value="gender">
          <a-radio value="Homme">Homme</a-radio>
          <a-radio value="Femme">Femme</a-radio>
          <a-radio value="Non précisé">Non précisé</a-radio>
          <a-radio value="Autre">Autre</a-radio>
        </a-radio-group>
        <div v-if="gender === 'Autre'" class="mt-2">
          <a-input v-model:value="customGender" placeholder="Votre genre" />
        </div>
      </a-form-item>

      <a-form-item label="Orientation politique">
        <a-input v-model:value="user.politicalSide" />
      </a-form-item>

      <a-form-item label="Taille (cm)">
        <a-input-number v-model:value="user.size" :min="0" style="width: 100%" />
      </a-form-item>

      <a-button type="primary" block>Enregistrer</a-button>
    </a-form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { fetchAuthSession } from '@aws-amplify/auth'
import { get } from '@aws-amplify/api-rest'
import { message } from 'ant-design-vue'
import LogoutButton from '../components/LogoutButton.vue'

const user = ref({
  firstName: '',
  lastName: '',
  email: '',
  birthDate: null,
  gender: null,
  politicalSide: null,
  size: null
})

const gender = ref('')
const customGender = ref('')

// 👇 Initialisation au chargement
onMounted(async () => {
  try {
    const session = await fetchAuthSession()
    const accessToken = session.tokens?.accessToken?.toString()

    console.log('[accessToken]', accessToken) 

    if (!accessToken) {
      message.error('Utilisateur non connecté')
      return
    }

    const response = await get({
      apiName: 'users',
      path: '/getUser',
      options: {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    })

    const { body } = await response.response
    const data = await body.json()

    user.value = data
    gender.value = data.gender || ''
    if (data.gender && !['Homme', 'Femme', 'Non précisé'].includes(data.gender)) {
      customGender.value = data.gender
    }

  } catch (error) {
    console.error('[Dashboard ERROR]', error)
    message.error("Impossible de charger le profil utilisateur.")
  }
})

// ✏️ Watchers pour le champ personnalisé "Autre"
watch(gender, (val) => {
  user.value.gender = val === 'Autre' ? customGender.value : val
})

watch(customGender, (val) => {
  if (gender.value === 'Autre') {
    user.value.gender = val
  }
})
</script>


<style scoped>
.max-w-2xl {
  max-width: 42rem;
}
</style>
