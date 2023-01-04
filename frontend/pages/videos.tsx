import Image from 'next/image'
import Link from 'next/link'
import { Key } from 'react'
import { redis, scan } from '../lib/database'

export default function videos({ videos }: any) {
  return (
    <div className='flex justify-center mt-4'>
      <div>
        {videos.map((video: any, id: Key) => (
          <div key={id} className='mt-4'>
              <div className='hover:cursor-pointer'>
                {video.title.S}
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
              </div>
            </div>
        ))}
      </div>
    </div>
  )
}

export async function getServerSideProps() {
  const video = await scan(process.env.TABLE_VIDEOS, process.env.VIDEO_INDEX)
  video.Items?.map((video, id)=>{
    console.log(video.updated_at_epoch.S)
  })

  return {
    props: {
      videos: video.Items,
    },
  }
}
