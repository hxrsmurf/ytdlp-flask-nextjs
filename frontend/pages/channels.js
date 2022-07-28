import EntryForm from '../Components/EntryForm'

import { CardActionArea, Container } from '@mui/material';

import Image from 'next/image'

import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

export default function channels({ results }) {
    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

    return (
        <>
            <Container sx={{marginTop: 3}}>
                <Container sx={{marginTop: 5}}>
                    <EntryForm />
                </Container>
            </Container>

            <Container sx={{marginTop: 5}}>
                {results.map((result, id) => (
                    <Card sx={{ backgroundColor: '#edebea', marginTop: 5 }} key={id}>
                        <CardActionArea href={result.original_url} target='_blank'>
                            <CardHeader
                                title={<Typography>{result.channel_name} - {result.original_url}</Typography>}
                            />
                            <CardContent>

                                {result.cdn_photo_cover ?
                                    <Image
                                        src={result.cdn_photo_cover}
                                        width={100}
                                        height={20}
                                        layout='responsive'
                                        lazyBoundary='25px'
                                        quality={100} />
                                    :
                                    <></>
                                }

                                <div sx={{marginTop: 3}}>{result.description}</div>

                            </CardContent>
                        </CardActionArea>
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