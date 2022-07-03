import Container from 'react-bootstrap/Container'
import EntryForm from '../Components/EntryForm'

export default function channels({ results }) {
    return (
        <>
            <Container className='mt-3'>
                <Container className='mt-5'>
                    <EntryForm type='Channels' />
                </Container>
            </Container>

            <Container className='mt-5'>
                <ul>
                    {results.map((result, id) => (
                        <li key={id}>
                            <a href={result.channel}>{result.channel}</a>
                        </li>
                    ))}
                </ul>
            </Container>
        </>
    )
}

export async function getServerSideProps() {
    const res = await fetch('http://127.0.0.1:5000/sqlalchemy?channels')
    const results = await res.json()
    return {
        props: {
            results
        }
    }
}