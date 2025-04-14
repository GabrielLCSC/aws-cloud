<template>
    <div class="container mt-5">
      <h2>Connexion</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label>Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label>Mot de passe</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Se connecter</button>
      </form>
      <p class="mt-3">
        Pas encore de compte ?
        <router-link to="/register">Créer un compte</router-link>
      </p>
    </div>
  </template>
  
  <script>
  import auth from '../store/auth';
  
  export default {
    data() {
      return { email: '', password: '' };
    },
    methods: {
      handleLogin() {
        // Ici tu mettrais ton appel API réel
        if (this.email && this.password) {
          auth.login({ email: this.email });
          this.$router.push('/');
        }
      }
    }
  };
  </script>
  