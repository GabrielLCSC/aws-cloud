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
      <!-- Adresses -->
<a-divider>Adresses</a-divider>
<a-form-item label="Ajouter une nouvelle adresse">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <a-input v-model:value="newAddress.street" placeholder="Rue" />
    <a-input v-model:value="newAddress.city" placeholder="Ville" />
    <a-input v-model:value="newAddress.zipCode" placeholder="Code Postal" />
    <a-input v-model:value="newAddress.country" placeholder="Pays" />
  </div>
  <a-button class="mt-2" type="dashed" @click="handleAddAddress" block>
    Ajouter l'adresse
  </a-button>
</a-form-item>

<div v-if="addresses.length" class="space-y-2">
  <div
    v-for="address in addresses"
    :key="address.id"
    class="border p-3 rounded flex justify-between items-center"
  >
    <div>
      <p class="font-semibold">{{ address.street }}</p>
      <p>{{ address.zipCode }} {{ address.city }}, {{ address.country }}</p>
    </div>
    <a-button type="text" danger @click="handleDeleteAddress(address.id)">
      Supprimer
    </a-button>
  </div>
</div>

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
const addresses = ref([])
const newAddress = ref({
  street: '',
  city: '',
  zipCode: '',
  country: ''
})

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
  addresses.value = data.addresses || []

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

    // 🧠 avatar est un path (ex: public/avatars/xxx.jpg)
    if (data.avatar) {
      const { url } = await getUrl({
        path: data.avatar,
        options: {
          level: 'public', // ou 'protected' si t'utilises ce niveau
          validateObjectExistence: true,
          expiresIn: 3600
        }
      })
      data.avatar = url
    }

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
      options: { level: 'protected', validateObjectExistence: true,expiresIn: 3600 }
    })

    user.value.avatar = url

    await post({
      apiName: 'users',
      path: '/updateUser',
      options: {
        body: { avatar: key }
      }
    })

    message.success("✅ Avatar mis à jour !")
  } catch (error) {
    console.error('[UPLOAD ERROR]', error)
    message.error('❌ Erreur lors de l’upload')
  }

  return false
}

async function handleAddAddress() {
  try {
    const payload = { ...newAddress.value }

    if (!payload.street || !payload.city || !payload.zipCode || !payload.country) {
      return message.warning("Tous les champs doivent être remplis.")
    }

    const res = await post({
      apiName: 'users',
      path: '/addAddress',
      options: {
        body: payload
      }
    })

    const { body } = await res.response
    const data = await body.json()

    addresses.value.push(data.address)
    Object.keys(newAddress.value).forEach(k => newAddress.value[k] = '')

    message.success("✅ Adresse ajoutée !")

  } catch (error) {
    console.error('[ADD ADDRESS ERROR]', error)
    message.error("❌ Erreur lors de l'ajout.")
  }
}

async function handleDeleteAddress(id) {
  try {
    const res = await post({
      apiName: 'users',
      path: '/deleteAddress',
      options: {
        body: { id }
      }
    })

    const { body } = await res.response
    const data = await body.json()

    addresses.value = addresses.value.filter(addr => addr.id !== id)
    message.success(data.message || "✅ Supprimée avec succès.")
  } catch (error) {
    console.error('[DELETE ADDRESS ERROR]', error)
    message.error("❌ Erreur lors de la suppression.")
  }
}




</script>


<style scoped>
.max-w-2xl {
  max-width: 42rem;
}
</style>
