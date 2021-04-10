import React from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import SortIcon from '@material-ui/icons/Sort';
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((theme) =>({
    root: {
        display: "flex",
        flexDirection: "row-reverse",
        padding: theme.spacing(2),
        paddingBottom: 0
    },
    menu: {
        borderRadius: theme.spacing(1)
    }
}))

type SortByProps = {
    callback: (sortType: number) => any
}

export default function SortBy(props: SortByProps) {
    const classes = useStyles();
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = (sortType: number) => {
        setAnchorEl(null);
        props.callback(sortType);
    };

    return (
        <div className={classes.root}>
            <Button startIcon={<SortIcon />} aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}>
                Sort by
            </Button>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
                classes={{paper: classes.menu}}
            >
                <MenuItem onClick={() => {handleClose(0)}}>Relevant</MenuItem>
                {/*<MenuItem onClick={() => {handleClose(1)}}>User Rating</MenuItem>*/}
            </Menu>
        </div>
    );
}
