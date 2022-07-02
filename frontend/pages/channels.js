import Container from 'react-bootstrap/Container'

export default function channels({ results }) {
    return (
        <>
            <Container className='mt-3'>
                <ul>
                    {results.map((result) => (
                        <li>
                            <a href={result}>{result}</a>
                        </li>
                    ))}
                </ul>
            </Container>
        </>
    )
}

export async function getStaticProps() {
    const res = await fetch('http://127.0.0.1:5000/channels')
    const results = await res.json()
    return {
        props: {
            results
        }
    }
}