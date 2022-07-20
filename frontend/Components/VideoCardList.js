import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col'
import { Youtube, Download, HandThumbsUp, Dot } from 'react-bootstrap-icons'

export default function VideoCardList({ data }) {

    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

    const handleDownloadClick = async (event) => {
        const query_url = (process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/download/video/' + event)
        fetch(query_url)
    }

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
                                                    <Button
                                                        variant='secondary'
                                                        onMouseDown={() => handleDownloadClick(result._id)}
                                                        >
                                                        <Download size={20} />
                                                    </Button>
                                                </Col>
                                            </Row>
                                        </div>
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