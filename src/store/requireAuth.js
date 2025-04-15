import { getCurrentUser } from '@aws-amplify/auth'

export async function requireAuth(_to, _from, next) {
  try {
    const user = await getCurrentUser()
    if (user) {
      next()
    }
  } catch (error) {
    console.warn('[AUTH GUARD] Not authenticated → redirect to login')
    next('/login')
  }
}
