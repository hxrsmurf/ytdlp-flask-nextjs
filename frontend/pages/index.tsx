import { useRouter } from 'next/router'
import { useEffect } from 'react'
import AddChannel from '../components/forms/AddChannel'
import LoadingPage from '../components/LoadingPage'
import { redis } from '../lib/database'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    router.push('/videos')
  })

  return <LoadingPage />

  return (
    <>
      <div className='flex justify-center mt-4'>
        <div>
          <div>
            <AddChannel />
          </div>
          <div>
            <div className='grid grid-cols-5'>
              {list_videos.map((video, id) => (
                <div key={id} className='mt-14'>
                  <div>{video.name}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export async function getServerSideProps() {
  const videos = await redis().get('videos')
  const channels = await redis().get('channels')

  return {
    props: {
      videos: videos,
      channels: channels,
    },
  }
}

const list_videos = [
  {
    name: 'Test',
  },
  {
    name: 'Test',
  },
  {
    name: 'Test',
  },
  {
    name: 'Test',
  },
  {
    name: 'Test',
  },
  {
    name: 'Test',
  },
]
