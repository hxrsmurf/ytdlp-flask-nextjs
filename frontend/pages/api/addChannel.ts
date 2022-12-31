import type { NextApiRequest, NextApiResponse } from 'next'
import { add_channel, channel_exists } from '../../utils/channels'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const query = req.query

  if (query['id']) {
    const id = String(query['id'])
    const exists = await channel_exists(id)

    if (exists < 0) {
      const result = await add_channel(id)
      if (result) {
        res.status(200).json({ result: 'Added Channel' })
      } else {
        res.status(500).json({ result: 'Error Adding Channel' })
      }
      return
    }
    res.status(200).json({ result: 'Channel Exists' })
    return
  }
  res.status(200).json({ result: 'Invalid Channel' })
  return
}