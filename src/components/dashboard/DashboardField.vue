<template>
    <div class="flex items-center justify-between border-b py-2">
      <div>
        <label class="text-sm text-gray-500">{{ label }}</label>
        <div v-if="!isEditing" class="text-lg flex items-center gap-2">
          <span>{{ value }}</span>
          <button @click="isEditing = true">
            <span :class="icon" class="text-gray-400 hover:text-black text-xl" />
          </button>
        </div>
        <div v-else class="flex items-center gap-2">
          <input
            v-model="editedValue"
            @keyup.enter="save"
            class="border rounded px-2 py-1 text-lg"
          />
          <button @click="save" class="text-blue-500">✅</button>
          <button @click="cancel" class="text-red-400">❌</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  
  const props = defineProps({
    label: String,
    value: String,
    icon: String
  })
  
  const emit = defineEmits(['update'])
  
  const isEditing = ref(false)
  const editedValue = ref(props.value)
  
  watch(() => props.value, (newVal) => {
    if (!isEditing.value) editedValue.value = newVal
  })
  
  function save() {
    emit('update', editedValue.value)
    isEditing.value = false
  }
  
  function cancel() {
    editedValue.value = props.value
    isEditing.value = false
  }
  </script>
  