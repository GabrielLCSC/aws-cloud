<template>
  <div class="max-w-xl mx-auto mt-10 space-y-6">
    <div class="flex items-center space-x-4">
      <img
        class="w-16 h-16 rounded-full object-cover"
        :src="user.avatar"
        alt="Avatar"
      />
      <h2 class="text-2xl font-semibold">Mon Profil</h2>
    </div>

    <DashboardField
      label="Nom"
      :value="user.name"
      icon="i-lucide-user"
      @update="(val) => user.name = val"
    />

    <DashboardField
      label="Email"
      :value="user.email"
      icon="i-lucide-mail"
      @update="(val) => user.email = val"
    />
  </div>
</template>

<script setup>
import DashboardField from '../components/dashboard/DashboardField.vue'

const user = reactive({
  name: 'Enzo Givernaud',
  email: 'enzo@example.com',
  avatar: 'https://i.pravatar.cc/150?u=enzo'
})
</script>
