import { channel } from 'diagnostics_channel'
import Image from 'next/image'
import Link from 'next/link'
import { Key } from 'react'
import { query, redis, scan } from '../lib/database'

export default function subscriptions({ channels }: any) {
  return (
    <div className='flex justify-center mt-4'>
      <div>
        {channels.map((channel: any, id: Key) => (
          <div key={id} className='mt-4'>
            <div className='hover:cursor-pointer'>
              {channel.channel.S}
              <Link href={channel.id.S} passHref legacyBehavior>
                <a target='_blank' rel='noopener noreferrer'>
                  <Image
                    src={channel.cover_photo.S}
                    alt=''
                    width={800}
                    height={800}
                  />
                </a>
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export async function getServerSideProps() {
  const channels = await scan(
    process.env.TABLE_CHANNELS,
    process.env.CHANNEL_INDEX
  )

  return {
    props: {
      channels: channels.Items,
    },
  }
}
