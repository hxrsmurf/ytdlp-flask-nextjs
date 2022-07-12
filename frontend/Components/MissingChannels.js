import Container from 'react-bootstrap/Container'
export default function MissingChannels({ data }) {
    return (
        <>
            <Container className='mt-5'>
                Manually add these channels
                <ul>
                    {data.map((channel, id) => (
                        <>
                            <li key={id}>
                                <a href={channel.original_url} rel='noopener'>{channel.channel_name} - {channel.title}</a>
                            </li>
                        </>
                    ))}
                </ul>
            </Container>
        </>
    )
}
