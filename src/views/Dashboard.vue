<template>
  <div class="max-w-2xl mx-auto mt-10 space-y-8 relative z-10 bg-[#131313] p-6 text-white">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-semibold">Mon Profil</h2>
      <LogoutButton />
    </div>

    <!-- Formulaire -->
     <a-form layout="vertical">

      <InputForm 
        v-model:value="user.firstName"
        type="text"
        text="Prénom"
      />

      <InputForm 
        v-model:value="user.lastName"
        type="text"
        text="Nom"
      />
      
      <InputForm 
        v-model:value="user.email"
        type="email"
        text="Email"
        :disabled="true"
        
        class="readonly-style"
      />


      <h2 class="text-white text-2xl font-semibold">Informations supplémentaires</h2>

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

      <a-button type="primary" block @click="handleUpdate" :loading="updating">
        Enregistrer
      </a-button>
    </a-form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { fetchAuthSession } from '@aws-amplify/auth'
import { get } from '@aws-amplify/api-rest'
import { message } from 'ant-design-vue'
import LogoutButton from '../components/LogoutButton.vue'
import { post } from '@aws-amplify/api-rest'

const updating = ref(false)

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

    if (!accessToken) {
      message.error('Utilisateur non connecté')
      return
    }

    const response = await get({
      apiName: 'users',
      path: '/getUser',
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

async function handleUpdate() {
  updating.value = true

  try {
    const payload = {
      firstName: user.value.firstName,
      lastName: user.value.lastName,
      birthDate: user.value.birthDate,
      gender: user.value.gender,
      politicalSide: user.value.politicalSide,
      size: user.value.size
    }

    const response = await post({
      apiName: 'users',
      path: '/updateUser',
      options: {
        body: payload
      }
    })

    const { body } = await response.response
    const data = await body.json()

    message.success(data.message || '✅ Profil mis à jour !')

  } catch (error) {
    console.error('[UPDATE ERROR]', error)
    message.error("❌ Impossible de mettre à jour le profil.")
  } finally {
    updating.value = false
  }
}

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



*, body{
  /* color: white !important; */
}

/* .readonly-style {
  pointer-events: none;
  opacity: 0.5;
} */
</style>
