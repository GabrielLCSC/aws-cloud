<template>
  <div class="max-w-2xl mx-auto mt-10 space-y-8 relative z-10 bg-[#131313] p-6 text-white popo">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-2xl font-semibold">Mon Profil</h2>
      <LogoutButton />
    </div>

    <div class="w-full mb-6 text-center">
      <router-link
        to="/apod"
        class="inline-block px-5 py-3 text-sm font-medium transition rounded-lg bg-[#A3E583] text-black hover:bg-[#c2f4a6]"
      >
        Découvre l'image du jour de la NASA
      </router-link>
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
        v-model="user.firstName"
        type="text"
        text="Prénom"
        :required="false"
      />

      <InputForm 
        v-model="user.lastName"
        type="text"
        text="Nom"
        :required="false"
      />
      
      <InputForm 
        v-model="user.email"
        type="email"
        text="Email"
        :disabled="true"
        
        class="readonly-style"
      />


        <!-- Divider -->
        <a-divider>Informations supplémentaires</a-divider>

        <!-- Date de naissance -->
        <a-form-item label="Date de naissance">

          <InputForm 
        v-model="user.birthDate"
        format="DD/MM/YYYY"
        type="date"
        text="Date"
        :required="false"
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
        v-model="user.customGender"
        type="text"
        text="Votre genre"
        :required="false"
      />    
    </div>
  </a-form-item>

        <InputForm 
        v-model="user.politicalSide"
        type="text"
        :required="false"
        text="Orientation politique"/>

        <InputForm 
        v-model="user.size"
        :required="false"
        text="Taille (cm)"

        :min="0" 
        style="width: 100%"
      />

        <!-- Divider -->
        <a-divider>Adresses</a-divider>

        <!-- Nouvelle adresse -->
        <!-- Bloc d’ajout d’adresse -->
<a-form-item label="Ajouter une nouvelle adresse">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <InputForm
      v-model="newAddress.street"
      type="text"
      text="Rue"
      :required="addressRequired"
    />
    <InputForm
      v-model="newAddress.city"
      type="text"
      text="Ville"
      :required="addressRequired"
    />
    <InputForm
      v-model="newAddress.zipCode"
      type="text"
      text="Code postal"
      :required="addressRequired"
    />
    <InputForm
      v-model="newAddress.country"
      type="text"
      text="Pays"
      :required="addressRequired"
    />
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
              class="bg-red-500"
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

const addressRequired = ref(false)
const addresses = ref([])
const newAddress = ref({ street: '', city: '', zipCode: '', country: '' })

const user = ref({
  firstName: '',
  lastName: '',
  email: '',
  birthDate: '',
  gender: '',
  politicalSide: '',
  size: '0',
  avatar: null,
})

const gender = ref('')
const customGender = ref('')

onMounted(async () => {
  try {
    const session = await fetchAuthSession()
    const accessToken = session.tokens?.accessToken?.toString()
    if (!accessToken) throw new Error('Utilisateur non connecté')

    loadingUser.value = true
    const response = await get({ apiName: 'users', path: '/getUser' })
    const { body } = await response.response
    const data = await body.json()

    addresses.value = Array.isArray(data.addresses) ? data.addresses : []

    // 👇 Vérifie si avatar est un path vers S3, puis le convertit en URL
    if (data.avatar && !data.avatar.startsWith('https')) {
      try {
        const { url } = await getUrl({
          path: data.avatar,
          options: { level: 'public', validateObjectExistence: true, expiresIn: 3600 },
        })
        data.avatar = url
      } catch (err) {
        console.warn('⚠️ Impossible de récupérer l’avatar S3 :', err)
      }
    }

    user.value = {
      ...user.value,
      ...data,
      birthDate: data.birthDate ? dayjs(data.birthDate).format('YYYY-MM-DD') : '',
      size: data.size ? String(data.size) : '0',
    }

    gender.value = data.gender || ''
    if (gender.value && !['Homme', 'Femme', 'Non précisé'].includes(gender.value)) {
      customGender.value = gender.value
    }
  } catch (err) {
    console.error('[getUser] error:', err)
    message.error("Impossible de charger le profil utilisateur.")
  } finally {
    loadingUser.value = false
  }
})

async function handleUpload(file) {
  try {
    uploading.value = true
    const extension = file.name.split('.').pop()
    const key = `public/avatars/${user.value.id || uuid()}.${extension}`

    const uploadTask = uploadData({
      path: key,
      data: file,
      options: { contentType: file.type }
    })
    const result = await uploadTask.result

    // 👇 Mise à jour dans DynamoDB : uniquement le `key`
    await post({
      apiName: 'users',
      path: '/updateUser',
      options: { body: { avatar: key } }
    })

    // 👇 On récupère maintenant la vraie URL d’affichage
    const { url } = await getUrl({
      path: key,
      options: { level: 'public', validateObjectExistence: true, expiresIn: 3600 }
    })

    user.value.avatar = url
    message.success("✅ Avatar mis à jour !")
  } catch (err) {
    console.error('[handleUpload] error:', err)
    message.error('❌ Erreur lors de l’upload')
  } finally {
    uploading.value = false
  }

  return false
}
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

.customAjouterAdress{
  background-color: #A3E583;
}


/* .readonly-style {
  pointer-events: none;
  opacity: 0.5;
} */
</style>
