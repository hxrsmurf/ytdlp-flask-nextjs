import Container from 'react-bootstrap/Container'
import EntryForm from '../Components/EntryForm'
import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import { Youtube, Download } from 'react-bootstrap-icons'

export default function videos({ results }) {

    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

    const handleMouseEnter = async (event) =>{

    }

    return (
        <>
            <Container className='mt-5'>
                <EntryForm type='Videos' />
            </Container>

            <Container className='mt-5'>
                {results.map((result, id) => (
                    <Card key={id} className='mt-5'>
                    <Card.Img
                        variant="top" src={result.thumbnail}
                        onClick={(e)=> handleClick(result.original_url)}
                        style={{ cursor: "pointer" }}
                        />
                        <Card.Header>
                            <Row>
                                <Col lg>{result.channel} - {result.title}</Col>
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
                        </Card.Header>
                    </Card>
                ))}
            </Container>
        </>
    )
}

export async function getServerSideProps() {
    const res = await fetch('http://127.0.0.1:5000/videos')
    const results = await res.json()

    return {
        props: {
            results
        }
    }
}