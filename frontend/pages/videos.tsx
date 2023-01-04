import Image from 'next/image'
import Link from 'next/link'
import { Key } from 'react'
import { redis, scan } from '../lib/database'

export default function videos({ videos }: any) {
  return (
    <div className='flex justify-center mt-4'>
      <div className='grid grid-cols-5 gap-8 max-w-[1400px] min-w[400px] min-h[200px]'>
        {videos.map((video: any, id: Key) => (
          <div key={id} className='mt-4'>
            <div className='hover:cursor-pointer'>
              <Link href={video.original_url.S} passHref legacyBehavior>
                <a target='_blank' rel='noopener noreferrer'>
                  <Image
                    src={video.thumbnail.S}
                    alt=''
                    width={360}
                    height={200}
                  />
                </a>
              </Link>
              <div>{video.title.S}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export async function getServerSideProps() {
  const video = await scan(process.env.TABLE_VIDEOS, process.env.VIDEO_INDEX)

  return {
    props: {
      videos: video.Items,
    },
  }
}
