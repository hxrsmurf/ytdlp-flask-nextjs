import { redis } from '../lib/database'

export async function get_channels(channel) {
  const db_channels = await redis().get('channels')
  return JSON.parse(db_channels)
}

export async function channel_exists(channel) {
  const channels = await get_channels()
  return Object.values(channels).indexOf(channel)
}

export async function add_channel(channel) {
  const channels = await get_channels()
  const append_channel = [...channels, channel]

  try {
    await redis().set('channels', JSON.stringify(append_channel))
    return true
  } catch (error) {
    console.log(error)
    return false
  }
}