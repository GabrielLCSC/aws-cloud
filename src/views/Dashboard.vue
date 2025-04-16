<template>
  <div class="max-w-2xl mx-auto mt-10 space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-semibold">Mon Profil</h2>
      <LogoutButton />
    </div>
    <a-form-item label="avatar">
  <div class="flex items-center space-x-4">
    <img
      v-if="user.avatar"
      :src="user.avatar"
      alt="avatar"
      class="w-16 h-16 rounded-full object-cover border"
    />
    <a-upload
      :before-upload="handleUpload"
      :show-upload-list="false"
      accept="image/*"
    >
      <a-button>Changer l'avatar</a-button>
    </a-upload>
  </div>
</a-form-item>




    <!-- Formulaire -->
    <a-form layout="vertical">
      <a-form-item label="Prénom">
        <a-input v-model:value="user.firstName" />
      </a-form-item>

      <a-form-item label="Nom">
        <a-input v-model:value="user.lastName" />
      </a-form-item>

      <a-form-item label="Email">
        <p class="ant-input ant-input-disabled">{{ user.email }}</p>
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
  size: null,
  avatar: null
})

const gender = ref('')
const customGender = ref('')

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

watch(gender, (val) => {
  user.value.gender = val === 'Autre' ? customGender.value : val
})

watch(customGender, (val) => {
  if (gender.value === 'Autre') {
    user.value.gender = val
  }
})

import { uploadData, getUrl } from 'aws-amplify/storage'
import { v4 as uuid } from 'uuid'

async function handleUpload(file) {
  try {
    const extension = file.name.split('.').pop()
    const key = `public/avatars/${user.value.id || uuid()}.${extension}`

    const uploadTask = uploadData({
      path: key,
      data: file,
      options: {
        contentType: file.type,
      }
    })

    const result = await uploadTask.result

    const { url } = await getUrl({
      path: result.path,
      options: { level: 'protected', validateObjectExistence: true }
    })

    user.value.avatar = url

    await post({
      apiName: 'users',
      path: '/updateUser',
      options: {
        body: { avatar: url }
      }
    })

    message.success("✅ Avatar mis à jour !")
  } catch (error) {
    console.error('[UPLOAD ERROR]', error)
    message.error('❌ Erreur lors de l’upload')
  }

  return false
}





</script>


<style scoped>
.max-w-2xl {
  max-width: 42rem;
}
</style>
