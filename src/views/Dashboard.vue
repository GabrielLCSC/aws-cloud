<template>
  <div class="max-w-2xl mx-auto mt-10 space-y-8 relative z-10 bg-[#131313] p-6 text-white popo">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-semibold">Mon Profil</h2>
      <LogoutButton />
    </div>

    <a-spin :spinning="loadingUser" tip="Chargement du profil...">
      <a-form layout="vertical">
        <!-- Avatar -->
        <a-form-item label="Avatar">
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
              <LoginButton text="Changer l'avatar" :loading="uploading"/>
            </a-upload>
          </div>
        </a-form-item>

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


        <!-- Divider -->
        <a-divider>Informations supplémentaires</a-divider>

        <!-- Date de naissance -->
        <a-form-item label="Date de naissance">
          <a-date-picker
            v-model:value="user.birthDate"
            format="DD/MM/YYYY"
            style="width: 100%"
          />
        </a-form-item>

        <!-- Genre -->
        <a-form-item label="Genre">
    <a-radio-group v-model:value="gender" class="custom-radio-group">
      <a-radio value="Homme">Homme</a-radio>
      <a-radio value="Femme">Femme</a-radio>
      <a-radio value="Non précisé">Non précisé</a-radio>
      <a-radio value="Autre">Autre</a-radio>
    </a-radio-group>
    <div v-if="gender === 'Autre'" class="mt-2">
      <InputForm 
        v-model:value="user.customGender"
        type="text"
        text="Votre genre"
      />    
    </div>
  </a-form-item>

        <InputForm 
        v-model:value="user.politicalSide"
        type="text"
        text="Orientation politique"/>

        <InputForm 
        v-model:value="user.size"
        type="number"
        text="Taille (cm)"

        :min="0" 
        style="width: 100%"
      />

        <!-- Divider -->
        <a-divider>Adresses</a-divider>

        <!-- Nouvelle adresse -->
        <a-form-item label="Ajouter une nouvelle adresse">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <InputForm v-model:value="newAddress.street" type="text" text="Rue"/>
            <InputForm v-model:value="newAddress.city" type="text" text="Ville"/>
            <InputForm v-model:value="newAddress.zipCode" type="text" text="Code postal"/>
            <InputForm v-model:value="newAddress.country" type="text" text="Pays"/>

          </div>
          <a-button
            class="mt-2 customAjouterAdress"
            type="dashed"
            @click="handleAddAddress"
            :loading="addingAddress"
            block
          >
            Ajouter l'adresse
          </a-button>
        </a-form-item>

        <!-- Liste des adresses -->
        <div v-if="addresses.length" class="space-y-2">
          <div
            v-for="address in addresses"
            :key="address.address_id"
            class="border p-3 rounded flex justify-between items-center"
          >
            <div>
              <p class="font-semibold">{{ address.street }}</p>
              <p>{{ address.zipCode }} {{ address.city }}, {{ address.country }}</p>
            </div>
            <a-button
              type="text"
              danger
              @click="handleDeleteAddress(address.address_id)"
              :loading="deletingId === address.address_id"
            >
              Supprimer
            </a-button>
          </div>
        </div>

        <!-- Bouton de sauvegarde -->
        <LoginButton text="Enregistrer" :loading="updating" @click="handleUpdate"/>

      </a-form>
    </a-spin>
  </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import { fetchAuthSession } from '@aws-amplify/auth'
import { get, post } from '@aws-amplify/api-rest'
import { message } from 'ant-design-vue'
import LogoutButton from '../components/LogoutButton.vue'
import { uploadData, getUrl } from 'aws-amplify/storage'
import { v4 as uuid } from 'uuid'
import dayjs from 'dayjs'

const loadingUser = ref(true)
const updating = ref(false)
const uploading = ref(false)
const addingAddress = ref(false)
const deletingId = ref(null)

const addresses = ref([])
const newAddress = ref({ street: '', city: '', zipCode: '', country: '' })

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
    if (!accessToken) return message.error('Utilisateur non connecté')

    const response = await get({ apiName: 'users', path: '/getUser' })
    const { body } = await response.response
    const data = await body.json()

    if (data.birthDate) data.birthDate = dayjs(data.birthDate)

    if (data.avatar) {
      const { url } = await getUrl({
        path: data.avatar,
        options: {
          level: 'public',
          validateObjectExistence: true,
          expiresIn: 3600
        }
      })
      data.avatar = url
    }

    addresses.value = data.addresses || []
    user.value = data
    gender.value = data.gender || ''
    if (data.gender && !['Homme', 'Femme', 'Non précisé'].includes(data.gender)) {
      customGender.value = data.gender
    }
  } catch {
    message.error("Impossible de charger le profil utilisateur.")
  } finally {
    loadingUser.value = false
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
      options: { body: payload }
    })

    const { body } = await response.response
    const data = await body.json()
    message.success(data.message || '✅ Profil mis à jour !')
  } catch {
    message.error("❌ Impossible de mettre à jour le profil.")
  } finally {
    updating.value = false
  }
}

async function handleUpload(file) {
  try {
    uploading.value = true
    const extension = file.name.split('.').pop()
    const key = `public/avatars/${user.value.id || uuid()}.${extension}`

    const uploadTask = uploadData({ path: key, data: file, options: { contentType: file.type } })
    const result = await uploadTask.result

    const { url } = await getUrl({
      path: result.path,
      options: { level: 'protected', validateObjectExistence: true, expiresIn: 3600 }
    })

    user.value.avatar = url

    await post({
      apiName: 'users',
      path: '/updateUser',
      options: { body: { avatar: key } }
    })

    message.success("✅ Avatar mis à jour !")
  } catch {
    message.error('❌ Erreur lors de l’upload')
  } finally {
    uploading.value = false
  }

  return false
}

async function handleAddAddress() {
  try {
    const payload = { ...newAddress.value }
    if (!payload.street || !payload.city || !payload.zipCode || !payload.country)
      return message.warning("Tous les champs doivent être remplis.")

    addingAddress.value = true
    const res = await post({ apiName: 'users', path: '/addAdress', options: { body: payload } })
    const { body } = await res.response
    const data = await body.json()

    addresses.value.push(data.address)
    Object.keys(newAddress.value).forEach(k => newAddress.value[k] = '')

    message.success("✅ Adresse ajoutée !")
  } catch {
    message.error("❌ Erreur lors de l'ajout.")
  } finally {
    addingAddress.value = false
  }
}

async function handleDeleteAddress(id) {
  try {
    deletingId.value = id
    const res = await post({
      apiName: 'users',
      path: '/deleteAdress',
      options: { body: { id } }
    })

    const { body } = await res.response
    const data = await body.json()

    addresses.value = addresses.value.filter(addr => addr.address_id !== id)
    message.success(data.message || "✅ Supprimée avec succès.")
  } catch {
    message.error("❌ Erreur lors de la suppression.")
  } finally {
    deletingId.value = null
  }
}

watch(gender, val => {
  user.value.gender = val === 'Autre' ? customGender.value : val
})

watch(customGender, val => {
  if (gender.value === 'Autre') {
    user.value.gender = val
  }
})
</script>

<style scoped>
.max-w-2xl {
  max-width: 42rem;
}

.popo{
  max-height: 700px;
  overflow-y: auto;
}


*, body{
  color: white !important;

  
}


/* .readonly-style {
  pointer-events: none;
  opacity: 0.5;
} */
</style>
