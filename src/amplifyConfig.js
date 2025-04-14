import { post } from '@aws-amplify/api-rest'
import { Amplify } from '@aws-amplify/core'

Amplify.configure({
  API: {
    REST: {
      users: {
        endpoint: 'https://4hi03himgj.execute-api.eu-west-1.amazonaws.com/bigzoo'
      }
    }
  }
})

export { post }
