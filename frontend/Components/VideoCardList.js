import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col'
import { Youtube, Download, HandThumbsUp, Dot } from 'react-bootstrap-icons'

export default function VideoCardList({ data }) {
    return (
        <>
            <Row>
                {data.map((result, id) => (
                    <Col lg='3'>
                        <Card key={id} className='mt-5'>
                            <Card.Img
                                variant="top" src={result.thumbnail}
                                onClick={(e) => handleClick(result.original_url)}
                                style={{ cursor: "pointer" }}
                            />
                            <Card.Header>
                                <Row>
                                    <Row><div className='fw-bold'>{result.channel}</div></Row>
                                    <Row><div>{result.title}</div></Row>
                                    <Row className='mt-2'><div>{result.duration_string} minutes<Dot />{result.view_count} Views</div></Row>
                                    <Row className='mt-1'>
                                        <div><HandThumbsUp /> {result.like_count}<Dot />{result.upload_date}</div>
                                    </Row>
                                    <Row>
                                        <div className='mt-3'>
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
                                                        variant='secondary'>
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