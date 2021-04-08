import {makeStyles} from "@material-ui/core/styles";

export const useStyles = makeStyles((theme) => {
    return ({
        search: {
            position: 'relative',
            borderRadius: theme.shape.borderRadius,
            width: '80%',
            maxWidth: '700px',
            marginLeft: "auto",
            marginRight: "auto",
            height: "50px",
            marginBottom: "30px",
        },
        searchIcon: {
            padding: theme.spacing(0, 2),
            height: '100%',
            position: 'absolute',
            pointerEvents: 'none',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
        },
        searchTitle: {
            color: 'white',
            textAlign: 'center',
            paddingBottom: theme.spacing(2),
            fontFamily: 'Helvetica Neue,Helvetica,Arial,sans-serif;',
            letterSpacing: '1px',
            fontWeight: 200
        },
        inputInput: {
            // vertical padding + font size from searchIcon
            paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
            width: '100%',
            paddingTop: "10px",
            borderRadius: theme.shape.borderRadius,
        },
        divider: {
            width: '80%',
        },
        infoTitle: {
            fontSize: '15px',
            fontWeight: "bold"
        },
        infoDetail: {
            color: 'rgba(0, 0, 0, 0.6)',
            fontSize: 14,
        },
        clps: {
            paddingLeft: '72px',
            paddingRight: '16px',
            paddingBottom: 10
        },
        circular: {
            position: 'absolute',
            right: 0,
            marginRight: '15px',
            marginTop: '15px',
        },
        mainIcon: {
            fontSize: 120,
            display: 'block',
            marginLeft: 'auto',
            marginRight: 'auto',
            color: 'white',
            marginTop: theme.spacing(3),
            marginBottom: theme.spacing(3),
        },
        searchBtn: {
            zIndex: 10,
            marginLeft: 'auto',
            marginRight: 'auto',
            display: 'block',
            borderRadius: theme.shape.borderRadius,
            backgroundColor: theme.palette.primary.dark,
            color: "white",
            '&:hover': {
                backgroundColor: "#1460aa"
            }
        },
        searchResult: {
            position: 'relative',
            width: '80%',
            maxWidth: '700px',
            marginLeft: "auto",
            marginRight: "auto",
            marginBottom: "30px",
            marginTop: "30px",
            borderRadius: theme.spacing(1)
        },
        reviewCrop: {
            textOverflow: "ellipsis",
            overflow: "hidden",
            "-webkit-line-clamp": 1,
            display: "-webkit-box",
            "-webkit-box-orient": "vertical",
        },
        reviewFull: {},
        locationIcon: {
            display: 'block',
            fontSize: 25,
            color: 'rgba(0, 0, 0, 0.6)',
        },
        wrapperAddress: {
            display: 'inline-block',
            height: 20,
            marginTop: 5
        },
        avatarPos: {
            backgroundColor: theme.palette.secondary.main
        },
        avatarNeutral: {
            backgroundColor: theme.palette.warning.dark
        },
        avatarNeg: {},
        statistics: {
            paddingTop: 20,
            paddingLeft: 20,
            marginBottom: 10
        },
        queryTime: {
            color: 'rgba(0, 0, 0, 0.7)',
            fontStyle: 'italic',
            fontSize: 15
        },
        switchBlock: {
            display: "flex",
            flexDirection: "row-reverse",
            padding: theme.spacing(2),
            paddingBottom: theme.spacing(1),
            paddingTop: theme.spacing(1),
        },
    })
}, {index: 1});
