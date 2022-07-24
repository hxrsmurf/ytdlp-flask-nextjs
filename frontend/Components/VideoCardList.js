import { HandThumbsUp, Dot } from 'react-bootstrap-icons'

import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'

import VideoButtons from './VideoButtons'

import Image from 'next/image'

export default function VideoCardList({ data }) {

    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

    return (
        <>
            <Row style={{ height: '150px' }}>
                {data.map((result, id) => (
                    <Col lg='4' key={id} style={{ width: '260px', height: '400px' }} className='mt-5'>
                        <Card key={id}>
                            <Card.Body>
                                {result.thumbnail ?
                                    <Image
                                        src={result.thumbnail}
                                        width={1200}
                                        height={800}
                                        layout='responsive'
                                        lazyBoundary='1px'
                                        quality={100}
                                        style={{ cursor: "pointer"}}
                                        onClick={(e) => handleClick(result.original_url)}
                                        />
                                :
                                    <></>
                                }
                            </Card.Body>
                            <Card.Header style={{ height: '240px', fontSize: '.9rem' }}>
                                <Row>
                                    <Row><div style={{ height: '40px', overflow: 'hidden', textOverflow: 'ellipsis' }}>{result.title}</div></Row>
                                    <Row className='mt-3'><div>{result.channel_name}</div></Row>
                                    <Row className='mt-3'><div>{result.view_count} Views<Dot />{result.upload_date}</div></Row>
                                    <Row className='mt-3'><div>{result.duration_string} minutes<Dot /><HandThumbsUp /> {result.like_count}</div></Row>
                                    <Row>
                                        <VideoButtons data={result}/>
                                    </Row>
                                </Row>
                            </Card.Header>
                        </Card>
                    </Col>
                ))}
            </Row>
        </>
    )
}