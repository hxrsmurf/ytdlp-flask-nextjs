import Container from 'react-bootstrap/Container'
import EntryForm from '../Components/EntryForm'
import Card from 'react-bootstrap/Card'

export default function channels({ results }) {
    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

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
                        <Card.Header>{result.channel_name} - {result.original_url}</Card.Header>
                        <Card.Img
                            variant="top" src={result.cdn_photo_cover}
                            />
                        <Card.ImgOverlay
                            onClick={(e)=> handleClick(result.original_url)}
                            style={{ cursor: "pointer" }}
                        />
                        <Card.Footer className="text-muted">{result.description}</Card.Footer>

                    </Card>
                ))}
            </Container>
        </>
    )
}

export async function getServerSideProps() {
    const res = await fetch(process.env.NEXT_PUBLIC_BASE_API_URL + '/mongo/channels/')
    const results = await res.json()
    return {
        props: {
            results
        }
    }
}