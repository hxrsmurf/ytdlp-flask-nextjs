import Image from 'next/image'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { Key, useState } from 'react'
import LoadingPage from '../components/LoadingPage'
import { redis, scan } from '../lib/database'

export default function Videos({ videos }: any) {
  const router = useRouter()
  const [showWatched, setShowWatched] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleClick = async (e: any) => {
    setLoading(true)

    setTimeout(async () => {
      await fetch('/api/video/watched?id=' + e.target.id)
      router.push('/videos')
      setLoading(false)
    }, 350)
  }

  if (loading) {
    return <LoadingPage />
  }

  return (
    <div className='flex justify-center mt-4'>
      <div>
        <button
          className='bg-slate-600 rounded p-3 mt-2'
          onClick={() => setShowWatched(showWatched ? false : true)}
        >
          Show Watched
        </button>
        <div className='grid grid-cols-5 gap-8 max-w-[1400px] min-w[400px] min-h[200px]'>
          {videos.map((video: any, id: Key) => (
            <>
              {!video.watched ? (
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
                    <div>
                      <button
                        id={video.id.S}
                        className='bg-slate-600 rounded p-3 mt-2'
                        onClick={(e) => handleClick(e)}
                      >
                        {video.watched ? (
                          <>Mark Not Watched</>
                        ) : (
                          <>Mark Watched</>
                        )}
                      </button>
                    </div>
                    <div>{video.title.S}</div>
                  </div>
                </div>
              ) : (
                <></>
              )}
            </>
          ))}
        </div>
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
