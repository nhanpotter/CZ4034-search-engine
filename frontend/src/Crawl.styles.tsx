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
            width: '70%',
            paddingTop: "10px",
            borderRadius: theme.shape.borderRadius,
            paddingRight: 10,
            display: 'inline-block',
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
        mainIcon: {
            fontSize: 120,
            display: 'block',
            marginLeft: 'auto',
            marginRight: 'auto',
            color: "white",
            marginTop: theme.spacing(3),
            marginBottom: theme.spacing(3),
            fontWeight: 400
        },
        inputNumber: {
            display: 'inline-block',
            width: "30%",
            paddingRight: 10,
            paddingLeft: 10,
            borderLeft: '1px solid',
            borderLeftColor: 'rgba(0,0,0,0.3)'
        },
        guide: {
            width: '70%',
            maxWidth: '600px',
            marginLeft: "auto",
            marginRight: "auto",
            padding: 0,
            borderRadius: theme.shape.borderRadius,
            marginTop: theme.spacing(3),
        },
        guideInfo: {
            textAlign: 'justify',
            margin: theme.spacing(3),
            paddingBottom: theme.spacing(2),
        },
        modal: {
            borderRadius: theme.spacing(1),
            width: 300,
            height: 200,
            marginLeft: 'auto',
            marginRight: 'auto',
            marginTop: 200,
            padding: 0
        },
        alert: {
            width: '60%',
            maxWidth: '500px',
            marginLeft: "auto",
            marginRight: "auto",
            marginBottom: theme.spacing(2),
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
        avatarPos: {
            backgroundColor: theme.palette.secondary.main
        },
        avatarNeutral: {
            backgroundColor: theme.palette.warning.dark
        },
        avatarNeg: {},
        clps: {
            paddingLeft: '72px',
            paddingRight: '16px',
            paddingBottom: 10
        },
        infoTitle: {
            fontSize: '15px',
            fontWeight: "bold"
        },
        infoDetail: {
            color: 'rgba(0, 0, 0, 0.6)',
            fontSize: 14,
        },
        divider: {
            width: '80%',
        },
        boxLabel: {
            textAlign: 'center',
            color: 'white',
            backgroundColor: theme.palette.primary.dark,
            borderTopLeftRadius: theme.shape.borderRadius,
            borderTopRightRadius: theme.shape.borderRadius,
            paddingTop: theme.spacing(1),
            paddingBottom: theme.spacing(1)
        },
        wait: {
            paddingTop: 5,
            paddingBottom: 5,
            textAlign: 'center',
            backgroundColor: theme.palette.primary.dark,
            borderTopLeftRadius: 8,
            borderTopRightRadius: 8,
            color: 'white'
        }
    })
}, {index: 1});
