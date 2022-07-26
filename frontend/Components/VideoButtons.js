import { Youtube, PlayFill, Display, DisplayFill, CloudArrowDown, FileEarmarkArrowDown } from 'react-bootstrap-icons'
import { useState } from 'react'


import VideoPlayer from './Modals/VideoPlayer'

import { Grid, IconButton } from '@mui/material';

export default function VideoButtons(props) {
    const result = props.data

    const [cdnVideo, setCDNVideo] = useState()
    const [modalShow, setModalShow] = useState()

    const handleDownloadClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/download/video/' + event)
        fetch(query_url)
    }

    const handlePlayCDNVideo = async (event) => {
        setCDNVideo(event)
        setModalShow(true)
    }

    const handleWatchedClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/' + event + '/watched')
        const result = await fetch(query_url)
    }

    const handleUnwatchedClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/' + event + '/unwatched')
        const result = await fetch(query_url)
    }

    const handleDownloadLocal = async (event) => {
        console.log(event)
    }

    return (
        <>
            <Grid
                container
                justifyContent="center"
                alignItems="center"
                className='mt-3'
            >
                <Grid item>
                    <IconButton href={result.original_url} target="_blank" size='large' rel='noreferred noopener'>
                        <Youtube color='red' />
                    </IconButton>
                </Grid>

                {result.cdn_video ?
                    <>
                        <Grid item>
                            <IconButton href={result.cdn_video} target="_blank" size='large' rel='noreferred noopener'>
                                <FileEarmarkArrowDown />
                            </IconButton>
                        </Grid>

                        <Grid item>
                            <IconButton size='large' onMouseDown={() => handlePlayCDNVideo(result)}>
                                <PlayFill />
                            </IconButton>

                            {cdnVideo ?
                                <>
                                    <VideoPlayer show={modalShow} data={cdnVideo} onHide={() => setModalShow(false)} />
                                </>
                                :
                                <></>
                            }
                        </Grid>
                    </>
                    :
                    <Grid item>
                        <IconButton onMouseDown={() => handleDownloadClick(result._id)}>
                            <CloudArrowDown />
                        </IconButton>
                    </Grid>
                }

                <Grid item>
                    {result.watched ?
                        <>
                            <IconButton onMouseDown={() => handleUnwatchedClick(result._id)}>
                                <DisplayFill />
                            </IconButton>
                        </>
                        :
                        <>
                            <IconButton onMouseDown={() => handleWatchedClick(result._id)}>
                                <Display />
                            </IconButton>
                        </>
                    }
                </Grid>
            </Grid>
        </>
    )
}