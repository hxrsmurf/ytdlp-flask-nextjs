import { useEffect, useState } from 'react'

import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import DownloadIcon from '@mui/icons-material/Download';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import TvTwoToneIcon from '@mui/icons-material/TvTwoTone';
import TvOutlinedIcon from '@mui/icons-material/TvOutlined';
import YouTubeIcon from '@mui/icons-material/YouTube';

import VideoPlayer from './Modals/VideoPlayer'
import LoadingCircle from './LoadingCircle';

import { Alert, Grid, IconButton, Snackbar } from '@mui/material';

export default function VideoButtons(props) {
    const result = props.data

    const [cdnVideo, setCDNVideo] = useState()
    const [modalShow, setModalShow] = useState()
    const [blobURL, setBlobURL] = useState()
    const [loading, setLoading] = useState()
    const [downloadQueued, setdownloadQueued] = useState(null)
    const [openSnackbar, setopenSnackbar] = useState()

    const handleDownloadClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/download/video/' + event)
        fetch(query_url)
        setdownloadQueued(true)
    }

    const handlePlayCDNVideo = async (event) => {
        setCDNVideo(event)
        setModalShow(true)
    }

    const handleWatchedClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/' + event + '/watched')
        const result = await fetch(query_url)
        setisWatched(true)
        setopenSnackbar(true)
    }

    const handleUnwatchedClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/' + event + '/unwatched')
        const result = await fetch(query_url)
        setisWatched(false)
        setopenSnackbar(true)
    }

    const handleSnackbarClose = async (event) => {
        setopenSnackbar(false)
    }

    const handleDownloadBlob = async (event) => {
        // https://stackoverflow.com/questions/71829361/how-to-download-mp4-video-in-js-react
        setLoading(true)
        const blob = await fetch(event)
            .then((response) => response.blob())
            .then((blob) => {
                const url = window.URL.createObjectURL(new Blob([blob]))
                setBlobURL(url)
                console.log(url)
            })
        setLoading(false)
    }

    const [isWatched, setisWatched] = useState()

    useEffect(() => {
        setisWatched(isWatched)
    }, [isWatched])



    return (
        <>
            <Grid
                container
                justifyContent="center"
                alignItems="center"
                sx={{marginTop: 3}}
            >
                <Grid item>
                    <IconButton href={result.original_url} target="_blank" size='large' rel='noreferred noopener'>
                        <YouTubeIcon sx={{ color: 'red' }} />
                    </IconButton>
                </Grid>

                {result.cdn_video == 'queued' ? <HourglassEmptyIcon/> : <>

                {result.cdn_video ?
                    <>
                        <Grid item>
                            {loading ?
                                <IconButton size='large'>
                                    <LoadingCircle />
                                </IconButton>
                                :
                                <>
                                    {blobURL ?
                                        <>
                                            <IconButton size='large' href={blobURL} download={result.title}>
                                                <DownloadIcon />
                                            </IconButton>
                                        </>
                                        :
                                        <>
                                            <IconButton size='large' onClick={() => handleDownloadBlob(result.cdn_video)}>
                                                <DownloadIcon />
                                            </IconButton>
                                        </>
                                    }
                                </>
                            }
                        </Grid>

                        <Grid item>
                            <IconButton size='large' onMouseDown={() => handlePlayCDNVideo(result)}>
                                <PlayArrowIcon />
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
                        {downloadQueued ?
                            <HourglassEmptyIcon/>
                        :
                            <IconButton onMouseDown={() => handleDownloadClick(result._id)}>
                                <CloudDownloadIcon />
                            </IconButton>
                        }
                    </Grid>
                }
                </>}

                <Snackbar
                    open={openSnackbar}
                    autoHideDuration={2000}
                    onClose={handleSnackbarClose}
                    anchorOrigin={{'horizontal': 'center', 'vertical': 'bottom'}}
                >
                    <Alert severity='success'>
                        {result.channel_name} {result.title}
                    </Alert>
                </Snackbar>

                <Grid item>
                    {isWatched ?
                        <>
                            <IconButton onMouseDown={() => handleUnwatchedClick(result._id)}>
                                <TvTwoToneIcon />
                            </IconButton>
                        </>
                        :
                        <>
                            {result.watched ?
                            <IconButton onMouseDown={() => handleUnwatchedClick(result._id)}>
                                <TvTwoToneIcon />
                            </IconButton>

                            :
                            <IconButton onMouseDown={() => handleWatchedClick(result._id)}>
                                <TvOutlinedIcon />
                            </IconButton>
                            }
                        </>
                    }
                </Grid>
            </Grid>
        </>
    )
}