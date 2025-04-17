<template>
    <div class="min-vh-100 d-flex align-items-center justify-content-center">
      <div class="w-100 px-3" style="max-width: 500px">
        <div class="z-10 relative text-white bg-[#131313] p-4 rounded shadow">
          <h2 class="text-2xl flex items-center justify-center gap-2 mb-4 text-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-green-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          Confirmation de compte
        </h2>
  
          <form @submit.prevent="handleConfirm">
            <InputForm v-model="email" type="email" text="Email" />
            <InputForm v-model="code" type="text" text="Code de confirmation" />
            
            <LoginButton type="submit" text="Confirmer mon compte" class="mt-4" :loading="loading" />
          </form>
  
          <p class="text-center mt-3">
            Pas reçu de code ?
            <a class="underline underline-offset-2" href="#" @click.prevent="resendCode">Renvoyer le code</a>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { confirmSignUp, resendSignUpCode } from '@aws-amplify/auth'
  import { message } from 'ant-design-vue'
  import InputForm from '@/components/InputForm.vue'
  
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
  