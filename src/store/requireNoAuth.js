import { getCurrentUser } from '@aws-amplify/auth'

export async function requireNoAuth(_to, _from, next) {
  try {
    const user = await getCurrentUser()
    if (!user) {
      next()
    }else{
        next('/')
    }
  } catch (error) {
    console.warn('[AUTH GUARD] Not authenticated → redirect to login')
    next('/')
  }
}
