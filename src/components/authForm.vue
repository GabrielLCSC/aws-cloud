<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <div class="w-full max-w-md bg-white p-8 rounded-xl shadow-lg">
        <h2 class="text-2xl font-bold text-center mb-6">
          {{ isLogin ? 'Connexion' : 'Inscription' }}
        </h2>
  
        <form @submit.prevent="handleSubmit">
          <!-- Email -->
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="form-control w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
  
          <!-- Password -->
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Mot de passe</label>
            <input
              v-model="form.password"
              type="password"
              class="form-control w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
  
          <!-- Confirm Password (Inscription only) -->
          <div v-if="!isLogin" class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Confirmer le mot de passe</label>
            <input
              v-model="form.confirmPassword"
              type="password"
              class="form-control w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
  
          <!-- Submit button -->
          <button
            type="submit"
            class="btn btn-primary w-full py-2 mt-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700"
          >
            {{ isLogin ? 'Se connecter' : "S'inscrire" }}
          </button>
        </form>
  
        <div class="mt-4 text-center">
          <p class="text-sm">
            {{ isLogin ? "Pas encore de compte ?" : "Déjà un compte ?" }}
            <button @click="toggleForm" class="text-blue-600 hover:underline ml-1">
              {{ isLogin ? "Inscris-toi" : "Connecte-toi" }}
            </button>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AuthForm',
    data() {
      return {
        isLogin: true,
        form: {
          email: '',
          password: '',
          confirmPassword: ''
        }
      };
    },
    methods: {
      toggleForm() {
        this.isLogin = !this.isLogin;
        this.form = {
          email: '',
          password: '',
          confirmPassword: ''
        };
      },
      handleSubmit() {
        if (!this.isLogin && this.form.password !== this.form.confirmPassword) {
          alert('Les mots de passe ne correspondent pas.');
          return;
        }
  
        if (this.isLogin) {
          alert(`Connexion avec : ${this.form.email}`);
          // → appel API login
        } else {
          alert(`Inscription avec : ${this.form.email}`);
          // → appel API register
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Optionnel si tu veux ajouter une bordure Bootstrap */
  .form-control {
    @apply border-gray-300;
  }
  </style>
  