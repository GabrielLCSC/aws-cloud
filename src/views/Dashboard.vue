<template>
  <div class="max-w-2xl mx-auto mt-10 space-y-8">
    <div class="flex items-center space-x-4">
      <h2 class="text-2xl font-semibold">Mon Profil</h2>
    </div>

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
import { ref, watch } from 'vue'

const user = {
  firstName: 'Enzo',
  lastName: 'Givernaud',
  email: 'enzo@example.com',
  birthDate: null,
  gender: null,
  politicalSide: null,
  size: null
}

const gender = ref(user.gender || '')
const customGender = ref('')

watch(gender, (val) => {
  user.gender = val === 'Autre' ? customGender.value : val
})

watch(customGender, (val) => {
  if (gender.value === 'Autre') {
    user.gender = val
  }
})
</script>

<style scoped>
.max-w-2xl {
  max-width: 42rem;
}
</style>
