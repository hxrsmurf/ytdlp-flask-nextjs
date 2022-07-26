import { Youtube, PlayFill, Display, DisplayFill, CloudArrowDown, FileEarmarkArrowDown } from 'react-bootstrap-icons'
import { useState } from 'react'

import Button from 'react-bootstrap/Button'

import VideoPlayer from './Modals/VideoPlayer'

import { Grid } from '@mui/material';

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
                spacing={1.2}
            >
                <Grid item>
                    <Button
                        href={result.original_url}
                        target="_blank"
                        variant='outline-danger'>
                        <Youtube size={15} />
                    </Button>
                </Grid>

                {result.cdn_video ?
                    <>
                        <Grid item>
                                <Button
                                    variant='outline-secondary'
                                    onMouseDown={() => handleDownloadLocal(result)}
                                    href={result.cdn_video}
                                    target="_blank"
                                    rel='noreferrer noopener'
                                >
                                    <FileEarmarkArrowDown size={15} />
                                </Button>
                        </Grid>

                        <Grid item>
                            <Button
                                variant='outline-secondary'
                                onMouseDown={() => handlePlayCDNVideo(result)}
                            >
                                <PlayFill size={15} />
                            </Button>

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
                        <Button
                            variant='outline-secondary'
                            onMouseDown={() => handleDownloadClick(result._id)}
                        >
                            <CloudArrowDown size={15} />
                        </Button>
                    </Grid>
                }

                <Grid item>
                    {result.watched ?
                        <>
                            <Button
                                variant='outline-secondary'
                                onMouseDown={() => handleUnwatchedClick(result._id)}
                            >
                                <DisplayFill size={15} />
                            </Button>
                        </>
                        :
                        <>
                            <Button
                                variant='outline-secondary'
                                onMouseDown={() => handleWatchedClick(result._id)}
                            >
                                <Display size={15} />
                            </Button>
                        </>
                    }
                </Grid>
            </Grid>
        </>
    )
}