<template>
    <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div class="w-100 px-3" style="max-width: 500px">
        <div class="bg-white p-4 rounded shadow">
          <h2 class="text-center mb-4">Connexion</h2>
  
          <form @submit.prevent="handleLogin">
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
              <label class="form-label">Mot de passe</label>
              <input
                v-model="password"
                type="password"
                class="form-control"
                required
              />
            </div>
  
            <button type="submit" class="btn btn-primary w-100">
              Se connecter
            </button>
          </form>
  
          <p class="mt-3 text-center">
            Pas encore de compte ?
            <router-link to="/register" class="text-primary text-decoration-none ms-1">
              Inscris-toi
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
      };
    },
    methods: {
      handleLogin() {
        if (this.email && this.password) {
          auth.login({ email: this.email });
          this.$router.push('/');
        }
      },
    },
  };
  </script>
  