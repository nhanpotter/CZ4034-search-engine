import {Box, Grid, IconButton, Typography} from "@material-ui/core";
import LocationOnOutlinedIcon from '@material-ui/icons/LocationOnOutlined';
import CloseOutlinedIcon from '@material-ui/icons/CloseOutlined';
import FavoriteBorderIcon from '@material-ui/icons/FavoriteBorder';
import {useStyles} from "./FilterIndicator.styles";

type FilterIndicatorProps = {
    name: string,
    id: string,
    tagType: number,
    onClickDelete: any
}

export default function FilterIndicator(props: FilterIndicatorProps) {
    const classes = useStyles();

    const handleClickDelete = () => {
        props.onClickDelete(props.tagType, props.id)
    }

    return (
        <div className={classes.filterLayout}>
            <Grid className={`${classes.filter} ${props.tagType === 0? classes.filterColorMain : classes.filterColorSuccess}`} container spacing={1}>
                <Grid item>
                    {props.tagType === 1 ?
                        <LocationOnOutlinedIcon  className={`${classes.indicatorIcon} ${classes.centerIcon}`}/>
                        :
                        <FavoriteBorderIcon  className={`${classes.indicatorIcon} ${classes.centerIcon}`}/>
                    }
                </Grid>

                <Grid>
                    <Typography className={`${classes.para}`}>{props.name}</Typography>
                </Grid>

                <Grid>
                    <IconButton onClick={handleClickDelete} size={"small"} className={`${classes.centerIcon} `}>
                        <CloseOutlinedIcon className={`${classes.closeIcon}`}/>
                    </IconButton>
                </Grid>
            </Grid>
        </div>
    )
}
