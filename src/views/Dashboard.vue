<template>
    <div class="container mt-5">
      <h2>Bienvenue sur ton tableau de bord</h2>
      <button @click="logout" class="btn btn-danger mt-3">Se déconnecter</button>
    </div>
  </template>
  
  <script>
  import auth from '../store/auth';
  
  export default {
    methods: {
      logout() {
        auth.logout();
        this.$router.push('/login');
      }
    }
  };
  </script>
  