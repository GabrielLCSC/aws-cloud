<template>
    <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div class="w-100 px-3" style="max-width: 500px">
        <div class="bg-white p-4 rounded shadow">
          <h2 class="text-center mb-4">Créer un compte</h2>
  
          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input
                v-model="email"
                type="email"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Nom</label>
              <input
                v-model="input"
                type="name"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Prénom</label>
              <input
                v-model="input"
                type="firstName"
                class="form-control"
                required
              />
            </div>
  
            <div class="mb-3">
              <label class="form-label">Mot de passe</label>
              <input
                v-model="password"
                type="password"
                class="form-control"
                required
              />
            </div>
  
            <div class="mb-3">
              <label class="form-label">Confirmer le mot de passe</label>
              <input
                v-model="confirmPassword"
                type="password"
                class="form-control"
                required
              />
            </div>
  
            <button type="submit" class="btn btn-primary w-100">
              S'inscrire
            </button>
          </form>
  
          <p class="mt-3 text-center">
            Déjà un compte ?
            <router-link to="/login" class="text-primary text-decoration-none ms-1">
              Connecte-toi
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import auth from '../store/auth';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
        confirmPassword: ''
      };
    },
    methods: {
      handleRegister() {
        if (this.password !== this.confirmPassword) {
          alert('Les mots de passe ne correspondent pas.');
          return;
        }
  
        // Ici tu mettrais ton appel API réel
        auth.login({ email: this.email });
        this.$router.push('/');
      }
    }
  };
  </script>
  