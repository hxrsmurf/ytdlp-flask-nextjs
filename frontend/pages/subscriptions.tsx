import Link from 'next/link'
import { Key } from 'react'
import { redis } from '../lib/database'

export default function subscriptions({ channels }: any) {
  return (
    <div className='flex justify-center mt-4'>
      <div>
        {channels.map((channel: String, id: Key) => (
          <div key={id} className='grid'>
            <div>
              <Link href={String(channel)} passHref legacyBehavior>
                <a target='_blank'>{channel}</a>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export async function getServerSideProps() {
  const db_result: string | null = await redis().get('channels')
  const channels = JSON.parse(db_result!)

  return {
    props: {
      channels: channels,
    },
  }
}
