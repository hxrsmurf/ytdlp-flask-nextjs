import { Youtube, Download, HandThumbsUp, Dot, PlayFill } from 'react-bootstrap-icons'
import { useState } from 'react'

import Button from 'react-bootstrap/Button'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import VideoPlayer from './Modals/VideoPlayer'

export default function VideoButtons(props) {
    const result = props.data

    const [cdnVideo, setCDNVideo] = useState()
    const [modalShow, setModalShow] = useState()

    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

    const handleDownloadClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/download/video/' + event)
        fetch(query_url)
    }

    const handlePlayCDNVideo = async (event) => {
        setCDNVideo(event)
        setModalShow(true)
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
                            <Youtube size={20} />
                        </Button>
                    </Col>
                    <Col md='auto'>
                        {result.cdn_video ?
                            <>
                                <Button
                                    variant='outline-secondary'
                                    onMouseDown={() => handlePlayCDNVideo(result)}
                                >
                                    <PlayFill size={20} />
                                </Button>
                                {
                                    cdnVideo ?
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
                                    <Download size={20} />
                                </Button>
                            </>}
                    </Col>
                </Row>
            </div>
        </>
    )
}