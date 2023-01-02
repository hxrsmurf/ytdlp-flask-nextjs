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
                {channel.info ? (
                  <Image
                    src={
                      JSON.parse(JSON.parse(channel.info.S))['thumbnails'][7][
                        'url'
                      ]
                    }
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

  return {
    props: {
      channels: channels.Items,
    },
  }
}
