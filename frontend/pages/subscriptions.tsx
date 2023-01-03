import Image from 'next/image'
import Link from 'next/link'
import { Key } from 'react'
import { redis, scan } from '../lib/database'

export default function subscriptions({ channels }: any) {
  return (
    <div className='flex justify-center mt-4'>
      <div>
        {channels.map((channel: any, id: Key) => (
          <div key={id} className='mt-4'>
            <div className='hover:cursor-pointer'>
              {channel.id.S}
              <Link href={channel.id.S} passHref legacyBehavior>
                {channel.cover_photo ? (
                  <Image
                    src={channel.cover_photo.S}
                    alt=''
                    width={800}
                    height={800}
                  />
                ) : (
                  <>{channel.id.S}</>
                )}
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export async function getServerSideProps() {
  const channels = await scan()
  console.log(channels)

  return {
    props: {
      channels: channels.Items,
    },
  }
}
