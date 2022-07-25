import { ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material"
import InboxIcon from '@mui/icons-material/Inbox';
import HomeIcon from '@mui/icons-material/Home';
import SubscriptionsIcon from '@mui/icons-material/Subscriptions';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';

export default function Sidebar({open, title, icon, url}) {
    return (
        <>
            <ListItem disablePadding sx={{ display: 'block' }}>
                <ListItemButton sx={{ minHeight: 48, justifyContent: open ? 'initial' : 'center', px: 2.5 }} href={url}>
                    <ListItemIcon sx={{ minWidth: 0, mr: open ? 3 : 'auto', justifyContent: 'center' }}>
                        {icon == 'Home' ? <HomeIcon/> : <></>}
                        {icon == 'Subscriptions' ? <SubscriptionsIcon/> : <></>}
                        {icon == 'Library' ? <VideoLibraryIcon/> : <></>}
                    </ListItemIcon>
                    <ListItemText primary={title} sx={{ opacity: open ? 1 : 0 }}/>
                </ListItemButton>
            </ListItem>
        </>
    )
}
