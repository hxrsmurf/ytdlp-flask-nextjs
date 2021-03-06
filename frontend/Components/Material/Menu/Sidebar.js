import { ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material"
import HomeIcon from '@mui/icons-material/Home';
import SubscriptionsIcon from '@mui/icons-material/Subscriptions';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';

export default function Sidebar({open, title, icon, url}) {
    return (
        <>
            <ListItem disablePadding sx={{ display: 'block',  mt:2 }}>
                <ListItemButton sx={{ minHeight: 48, justifyContent: open ? 'initial' : 'center', px: 2.5 }} href={url}>
                    <ListItemIcon sx={{ minWidth: 0, mr: open ? 3 : 'auto', justifyContent: 'center' }}>
                        {icon == 'Home' ? <HomeIcon sx={{fontSize: 35}}/> : <></>}
                        {icon == 'Subscriptions' ? <SubscriptionsIcon sx={{fontSize: 35}}/> : <></>}
                        {icon == 'Library' ? <VideoLibraryIcon sx={{fontSize: 35}}/> : <></>}
                    </ListItemIcon>
                    <ListItemText primary={title} sx={{ opacity: open ? 1 : 0 }}/>
                </ListItemButton>
            </ListItem>
        </>
    )
}
