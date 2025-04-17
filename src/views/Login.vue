<template>
    <div class="relative z-10 min-vh-100 d-flex align-items-center justify-content-center">
    <div class="w-100 px-3" style="max-width: 500px">
      <div class="background-color p-4 rounded shadow">
      <div class="flex items-center justify-center gap-2 text-white mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 stroke-current" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4m-4-4l4-4m0 0l-4-4m4 4H3" />
        </svg>
        <h2 class="text-xl font-semibold">Connexion</h2>
      </div>

        <form @submit.prevent="handleLogin">
          <InputForm v-model="email" type="email" text="Email" />
          <InputForm v-model="password" type="password" text="Mot de passe" />
          <LoginButton text="Se connecter" class="mt-4" :loading="loading" />
        </form>

        <p class="text-white mt-3 text-center">
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
import { signIn } from '@aws-amplify/auth'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router';
import LoginButton from '../components/LoginButton.vue'
import InputForm from '@/components/InputForm.vue';

const router = useRouter()

export default {
  data() {
    return {
      email: '',
      password: '',
      loading: false
    };
  },
  methods: {
    async handleLogin() {
      if (!this.email || !this.password) return;

      this.loading = true

      try {
        await signIn({ username: this.email, password: this.password });
        message.success(`Connected`);
        console.log()
        this.$router.push('/')
      } catch (err) {
        console.error('[LOGIN ERROR]', err);

        if (err.name === 'UserNotFoundException') {
          message.error("Aucun compte trouvé avec cet email.");
        } else if (err.name === 'NotAuthorizedException') {
          message.error("Email ou mot de passe incorrect.");
        } else if (err.name === 'UserNotConfirmedException') {
          message.warning("Compte non confirmé. Vérifie tes emails.");
        } else {
          message.error(err.message || 'Erreur lors de la connexion.');
        }
      } finally {
        this.loading = false
      }
    }
  }
};
</script>
<style scoped>
.background-color {
  background-color: #131313;
}

</style>