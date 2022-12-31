import { createClient } from 'redis'

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