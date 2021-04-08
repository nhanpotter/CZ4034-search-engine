import {makeStyles} from "@material-ui/core/styles";

export const useStyles = makeStyles((theme) => ({
    filterLayout: {
        height: 30,
        padding: theme.spacing(1),
        display: "inline-block"
    },
    filter: {
        border: '1px solid',
        borderRadius: theme.shape.borderRadius,
        width: 'fit-content',
        padding: 1,
    },
    filterColorMain: {
        color: theme.palette.secondary.main,
        borderColor: theme.palette.secondary.main,
        "&:hover": {
            backgroundColor: theme.palette.secondary.dark,
            color: 'white',
        }
    },
    filterColorSuccess: {
        color: theme.palette.success.main,
        borderColor: theme.palette.success.main,
        "&:hover": {
            backgroundColor: theme.palette.success.dark,
            color: 'white',
        }
    },
    para: {
        fontSize: 14,
        maxWidth: 400,
        textOverflow: "ellipsis",
        overflow: "hidden",
        "-webkit-line-clamp": 1,
        display: "-webkit-box",
        "-webkit-box-orient": "vertical",
        height: "100%",
        marginTop: 2,
        marginBottom: "auto",
    },
    indicatorIcon: {
        fontSize: 18
    },
    closeIcon: {
        fontSize: 18,
        color: 'inherit'
    },
    centerIcon: {
        display: "block",
        height: "100%",
        marginTop: "auto",
        marginBottom: "auto",
        color: 'inherit'
    }
}), {index: 1});
