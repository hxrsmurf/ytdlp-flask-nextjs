import type { NextApiRequest, NextApiResponse } from 'next'
import { redis } from '../../lib/database'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const query = req.query

  if (query['id']) {
    const id = String(query['id'])
    await redis().HSET('channels', id, id)
    res.status(200).json({ result: 'Added Channel' })
  }
  res.status(200).json({ result: 'Invalid Channel' })
}