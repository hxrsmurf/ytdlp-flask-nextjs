import Container from 'react-bootstrap/Container'
import EntryForm from '../Components/EntryForm'

export default function videos({ results }) {
    return (
        <>
            <Container className='mt-5'>
                <EntryForm type='Videos' />
            </Container>

            <Container className='mt-5'>
                <ul>
                    {results.map((result, id) => (
                        <li key={id}>
                            {result.channel}
                            <ul>
                                {result.videos.map(video => (
                                    <li><a href={'http://127.0.0.1:5000/static/' + result.channel + '/' + video}>{video}</a></li>
                                ))}
                            </ul>
                        </li>
                    ))}
                </ul>
            </Container>
        </>
    )
}

export async function getServerSideProps() {
    const res = await fetch('http://127.0.0.1:5000/available_videos')
    const results = await res.json()

    return {
        props: {
            results
        }
    }
}