import Image from 'next/image'
import Link from 'next/link'
import { Key } from 'react'
import { redis } from '../lib/database'

export default function subscriptions({ channels }: any) {
  return (
    <div className='flex justify-center mt-4'>
      <div>
        {channels.map((channel: any, id: Key) => (
          <div key={id} className='mt-4'>
            <div className='hover:cursor-pointer'>
              {channel.url}
              <Link href={String(channel.url)} passHref legacyBehavior>
                <Image src={channel.cover[0]} alt='' width={1000} height={1000} />
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
