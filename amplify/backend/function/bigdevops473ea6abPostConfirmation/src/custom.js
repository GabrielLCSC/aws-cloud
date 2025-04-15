/**
 * @type {import('@types/aws-lambda').APIGatewayProxyHandler}
 */
const {LambdaClient, InvokeCommand} = require("@aws-sdk/client-lambda")

const lambdaClient = new LambdaClient()

exports.handler = async (event, context) => {
  console.log(event)
  if(event.triggerSource === "PostConfirmation_ConfirmSignUp") {

    console.log('event.triggerSource === "PostConfirmation_ConfirmSignUp"')

    const user_id = event.userName
    const sub = event.request.userAttributes.sub
    const first_name = event.request.userAttributes.name
    const last_name = event.request.userAttributes.family_name
    const email = event.request.userAttributes.email

    console.log("FUNCTION_INSERTUSER_NAME", process.env.FUNCTION_INSERTUSER_NAME)

    const asyncLambdaParams = {
      FunctionName: process.env.FUNCTION_INSERTUSER_NAME,
      InvocationType: "Event",
      Payload: JSON.stringify({user_id, first_name, last_name, email, sub})
    }

    console.log("asyncLambdaParams", asyncLambdaParams)

    const command = new InvokeCommand(asyncLambdaParams)
    await lambdaClient.send(command)
  }
  return event;
};
