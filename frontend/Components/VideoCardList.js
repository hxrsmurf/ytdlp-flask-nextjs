import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col'
import { Youtube, Download, HandThumbsUp, Dot, PlayFill } from 'react-bootstrap-icons'
import { useState } from 'react'
import VideoButtons from './VideoButtons'

export default function VideoCardList({ data }) {
    return (
        <>
            <Row style={{ height: '150px' }}>
                {data.map((result, id) => (
                    <Col lg='4' key={id} style={{ width: '260px', height: '400px' }} className='mt-5'>
                        <Card key={id}>
                            <Card.Img
                                variant="top" src={result.thumbnail}
                                onClick={(e) => handleClick(result.original_url)}
                                style={{ cursor: "pointer", height: '150px', width: '100%' }}
                            />
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