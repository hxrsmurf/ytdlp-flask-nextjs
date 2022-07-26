import { Box, List, ListItem, ListItemButton, ListItemText, ListSubheader } from '@mui/material';

export default function MissingChannels({ data }) {
    return (
        <>
            <Box className='mt-5' sx={{ border: true, width: '700px', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                <List
                    className='mt-2'
                    subheader={<ListSubheader>Manually add these channels</ListSubheader>}
                >
                    {data.map((channel, id) => (
                        <>
                            <ListItem key={id} disablePadding>
                                <ListItemButton component="a" href={channel.original_url}>
                                    <ListItemText>
                                        {channel.channel_name} - {channel.title}
                                    </ListItemText>
                                </ListItemButton>
                            </ListItem>
                        </>
                    ))}
                </List>
            </Box>
        </>
    )
}
