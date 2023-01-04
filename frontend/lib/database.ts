import { createClient } from 'redis'
import { DynamoDB } from 'aws-sdk'

const aws_key_id = process.env.AWS_ACCESS_KEY_ID
const aws_key = process.env.AWS_ACCESS_KEY

export function redis() {
  const client = createClient({
    socket: {
      host: process.env.REDIS_URL,
      port: Number(process.env.REDIS_PORT),
    },
  })
  client.connect()
  return client
}

export function aws_db() {
  return new DynamoDB({
    accessKeyId: aws_key_id,
    secretAccessKey: aws_key,
    region: process.env.REGION,
  })
}

export async function scan(
  table: string | undefined,
  index: string | undefined
) {
  const params: any = {
    TableName: table,
    IndexName: index,
  }

  const result = await aws_db()
    .scan(params)
    .promise()
    .then((items) => {
      return items
    })

  // Get the thumbnail details
  // const test = result.Items[0].info.S
  // const z = JSON.parse(test)
  // console.log(JSON.parse(z))

  return result
}

export async function query(
  table: string | undefined,
  index: string | undefined
) {
  const params: any = {
    TableName: table,
    IndexName: index,
  }

  if (table?.includes('channel')) {
    params['ScanIndexForward'] = true
    params['KeyConditionExpression'] = 'begins_with(id, :url)'
    params['ExpressionAttributeValues'] = {
      ':url': { 'S': 'http' },
    }
  }
  const result = await aws_db()
    .query(params)
    .promise()
    .then((items) => {
      return items
    })
}
