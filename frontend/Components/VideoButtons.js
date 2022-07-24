import { Youtube, Download, PlayFill, Display, DisplayFill } from 'react-bootstrap-icons'
import { useState } from 'react'

import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'

import VideoPlayer from './Modals/VideoPlayer'

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
        const result =  await fetch(query_url)
    }

    const handleUnwatchedClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/videos/' + event + '/unwatched')
        const result =  await fetch(query_url)
    }

    return (
        <>
            <div className='mt-4'>
                <Row>
                    <Col md='auto'>
                        <Button
                            href={result.original_url}
                            target="_blank"
                            variant='outline-danger'>
                            <Youtube size={15} />
                        </Button>
                    </Col>
                    <Col md='auto'>
                        {result.cdn_video ?
                            <>
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
                            </>
                            :
                            <>
                                <Button
                                    variant='outline-secondary'
                                    onMouseDown={() => handleDownloadClick(result._id)}
                                >
                                    <Download size={15} />
                                </Button>
                            </>}
                    </Col>
                    <Col md='auto'>
                        {result.watched ?
                        <>
                            <Button
                                variant='outline-secondary'
                                onMouseDown={() => handleUnwatchedClick(result._id)}
                            >
                                <DisplayFill size={15}/>
                            </Button>
                        </>
                        :
                        <>
                            <Button
                                variant='outline-secondary'
                                onMouseDown={() => handleWatchedClick(result._id)}
                            >
                                <Display size={15}/>
                            </Button>
                        </>
                        }
                    </Col>
                </Row>
            </div>
        </>
    )
}