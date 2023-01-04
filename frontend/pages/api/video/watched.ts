import type { NextApiRequest, NextApiResponse } from 'next'
import { video_watched } from '../../../lib/database'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const query = req.query

  if (query['id']) {
    const id = String(query['id'])
    video_watched(id)
    res.status(200).json({ result: 'Marked video as watched' })
    return
  }

  res.status(200).json({ result: 'Invalid video id' })
  return
}