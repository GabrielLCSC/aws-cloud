<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="w-100 px-3" style="max-width: 500px">
      <div class="bg-white p-4 rounded shadow">
        <h2 class="text-center mb-4 text-red-600">Connexion</h2>

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

          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            <span v-if="loading">Connexion...</span>
            <span v-else>Se connecter</span>
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
import { signIn } from '@aws-amplify/auth'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router';

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
