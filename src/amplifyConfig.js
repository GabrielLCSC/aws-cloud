import { Amplify } from 'aws-amplify'

Amplify.configure({
  API: {
    endpoints: [
      {
        name: 'myapi',
        endpoint: 'https://abc123.execute-api.eu-west-1.amazonaws.com/dev',
      }
    ]
  }
})
