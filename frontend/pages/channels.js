import Container from 'react-bootstrap/Container'
import EntryForm from '../Components/EntryForm'
import Card from 'react-bootstrap/Card'

export default function channels({ results }) {
    return (
        <>
            <Container className='mt-3'>
                <Container className='mt-5'>
                    <EntryForm type='Channels' />
                </Container>
            </Container>

            <Container className='mt-5'>
                {results.map((result, id) => (
                    <Card style={{ width: '75' }} key={id} className='mt-5'>
                        <Card.Header>{result.channel}</Card.Header>
                        <Card.Img variant="top" src={result.picture_cover}/>
                        <Card.ImgOverlay/>
                        <Card.Footer className="text-muted">{result.description}</Card.Footer>

                    </Card>
                ))}
            </Container>
        </>
    )
}

export async function getServerSideProps() {
    const res = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + 'channels')
    const results = await res.json()
    return {
        props: {
            results
        }
    }
}