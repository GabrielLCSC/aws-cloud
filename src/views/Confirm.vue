<template>
    <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div class="w-100 px-3" style="max-width: 500px">
        <div class="bg-white p-4 rounded shadow">
          <h2 class="text-center mb-4">Confirmation de compte</h2>
  
          <form @submit.prevent="handleConfirm">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="email" type="email" class="form-control" required />
            </div>
  
            <div class="mb-3">
              <label class="form-label">Code de confirmation</label>
              <input v-model="code" type="text" class="form-control" required />
            </div>
  
            <button type="submit" class="btn btn-success w-100" :disabled="loading">
              <span v-if="loading">Confirmation...</span>
              <span v-else>Confirmer mon compte</span>
            </button>
          </form>
  
          <p class="text-center mt-3">
            Pas reçu de code ?
            <a href="#" @click.prevent="resendCode">Renvoyer le code</a>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { confirmSignUp, resendSignUpCode } from '@aws-amplify/auth'
  import { message } from 'ant-design-vue'
  
  export default {
    data() {
  return {
    email: this.$route.query.email || '',
    code: '',
    loading: false
  }
},

    methods: {
      async handleConfirm() {
        this.loading = true
        try {
          await confirmSignUp({ username: this.email, confirmationCode: this.code })
          message.success("✅ Ton compte est confirmé ! Tu peux te connecter.")
          this.$router.push('/login')
        } catch (err) {
          console.error('[CONFIRMATION ERROR]', err)
          message.error(err.message || 'Erreur lors de la confirmation')
        } finally {
          this.loading = false
        }
      },
  
      async resendCode() {
        try {
          await resendSignUpCode({ username: this.email })
          message.success("📧 Nouveau code envoyé à ton adresse email.")
        } catch (err) {
          console.error('[RESEND ERROR]', err)
          message.error(err.message || "Erreur lors de l'envoi du code")
        }
      }
    }
  }
  </script>
  