import VideoButtons from './VideoButtons'

import { CardActionArea, Grid } from '@mui/material'

import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Typography from '@mui/material/Typography';

import Image from 'next/image';

export default function VideoCardList({ data }) {

    const handleClick = async (event) => {
        window.open(event, '_blank')
    }

    return (
        <>
            <Grid container spacing={4}>
                {data.map((result, id) => (
                    <Grid item spacing={4}>
                        <Card sx={{ width: 250, height: 320, backgroundColor: '#edebea' }}>
                            <CardActionArea>
                                <CardHeader
                                    title={<Typography noWrap>{result.title}</Typography>}
                                    subheader={result.channel_name}
                                    sx={{ display: 'block', overflow: 'hidden' }}
                                />
                                <CardContent>

                                {result.thumbnail ?
                                    <Image
                                        src={result.thumbnail}
                                        width={700}
                                        height={400}
                                        layout='responsive'
                                        lazyBoundary='1px'
                                        quality={100}
                                        style={{ cursor: "pointer"}}
                                        onClick={(e) => handleClick(result.original_url)}
                                        />
                                :
                                    <></>
                                }
                                    <Grid container spacing={1} justifyContent='center' alignItems='center'>
                                        <Grid item>{result.view_count} views</Grid>
                                        <Grid item><span className='dot'></span></Grid>
                                        <Grid item>{result.upload_date}</Grid>
                                    </Grid>
                                </CardContent>
                            </CardActionArea>
                            <CardActions sx={{ height: 2 }}>
                                <VideoButtons data={result} />
                            </CardActions>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </>
    )
}