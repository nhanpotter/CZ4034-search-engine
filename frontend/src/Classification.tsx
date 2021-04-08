import {
    Button,
    CircularProgress,
    InputBase,
    Modal,
    Paper, Table, TableBody, TableHead, TableRow, Tooltip,
    Typography
} from "@material-ui/core";
import React, {useEffect} from "react";
import Alert from '@material-ui/lab/Alert';
import SettingsOutlinedIcon from '@material-ui/icons/SettingsOutlined';
import {useStyles} from './Classification.styles';
import {TableCell} from "@material-ui/core";
import FastfoodOutlinedIcon from '@material-ui/icons/FastfoodOutlined';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import RoomServiceOutlinedIcon from '@material-ui/icons/RoomServiceOutlined';
import MonetizationOnOutlinedIcon from '@material-ui/icons/MonetizationOnOutlined';
import SentimentSatisfiedOutlinedIcon from '@material-ui/icons/SentimentSatisfiedOutlined';
import SentimentDissatisfiedOutlinedIcon from '@material-ui/icons/SentimentDissatisfiedOutlined';
import SentimentSatisfiedIcon from '@material-ui/icons/SentimentSatisfied';
import QueryAPI from "./api/Query.api";

enum alertType {error = 'error', success = 'success'};

export default function Classification() {
    const classes = useStyles();
    const [inputReview, setInputReview] = React.useState("");
    const [openLoading, setOpenLoading] = React.useState(false);
    const [alertStatus, setAlertStatus] = React.useState<alertType | undefined>(undefined);
    const [alertInfo, setAlertInfo] = React.useState("");
    const [resultState, setResultState] = React.useState(new Array(12).fill(0))
    const [overallSentiment, setOverallSentiment] = React.useState(new Array(3).fill(false));

    const handleClassify = () => {
        setOpenLoading(true);

        QueryAPI.classify(inputReview, (res: {data: any, status: number}) => {
            if (res.status === 1 && res.data.errors === undefined) {
                let newSentiment = new Array(3).fill(false);
                newSentiment[res.data['sentiment_model'] - 1] = true
                setOverallSentiment(newSentiment);
                let newAspect = new Array(12).fill(0);
                newAspect[res.data['aspect_model']['food']] = 1;
                newAspect[res.data['aspect_model']['service'] + 4] = 1;
                newAspect[res.data['aspect_model']['price'] + 8] = 1;
                setResultState(newAspect);
            } else if (res.status === 1) {
                setAlertInfo(res.data.errors);
                setOverallSentiment([false, false, false]);
                setResultState(new Array(12).fill(0))
                setAlertStatus(alertType.error);
            }

            setOpenLoading(false);
        })
    }

    useEffect(() => {
        setResultState([1,0,0,0,0,1,0,0,0,0,0,1]);
    }, [])

    return (
        <div>
            <div>
                <SettingsOutlinedIcon className={`${classes.searchTitle} ${classes.mainIcon}`}/>
                <Typography component={"h6"} variant={"h6"} className={classes.searchTitle}>
                    Analyze your review sentiment and classify your review based on aspect
                </Typography>
            </div>

            <Paper elevation={3} className={classes.search}>
                <InputBase
                    placeholder="Input your review here and let our engine analyze..."
                    className={classes.inputInput}
                    inputProps={{'aria-label': 'search'}}
                    value={inputReview}
                    multiline
                    rows={2}
                    rowsMax={5}
                    onChange={(e) => {
                        setInputReview(e.target.value)
                    }}
                />
            </Paper>

            {alertStatus && <Alert className={classes.alert} severity={alertStatus} onClose={() => {
                setAlertStatus(undefined)
            }}>{alertInfo}</Alert>}

            <Button disabled={inputReview.length === 0} onClick={() => handleClassify()} variant={'contained'}
                    size={'large'}
                    className={classes.searchBtn}>Analyze</Button>

            {(overallSentiment[0] | overallSentiment[1] | overallSentiment[2]) ? <Paper elevation={3} className={classes.guide}>
                <Typography className={classes.boxLabel} component={"h5"} variant={"h5"}>Result</Typography>

                <Typography component={"p"} className={classes.overall}>Overall sentiment</Typography>
                <div style={{marginLeft: "auto", marginRight: 'auto', display:'block', width: 'fit-content', marginTop: 10}}>
                    <Tooltip title={"Negative"} ><SentimentDissatisfiedOutlinedIcon style={overallSentiment[0] ? {color: '#dc004e'}: {}} className={classes.sentimentIcon}/></Tooltip>
                    <Tooltip title={"Neutral"} ><SentimentSatisfiedIcon style={overallSentiment[1] ? {color: '#dc004e'}: {}} className={classes.sentimentIcon}/></Tooltip>
                    <Tooltip title={"Positive"} ><SentimentSatisfiedOutlinedIcon style={overallSentiment[2] ? {color: '#dc004e'}: {}} className={classes.sentimentIcon}/></Tooltip>
                </div>

                <div className={classes.tableContainer}>
                    <Table className={classes.table}>
                        <TableHead>
                            <TableRow>
                                <TableCell className={classes.firstCol}/>
                                <TableCell align="center" className={classes.sentiment}>Not Mention</TableCell>
                                <TableCell align="center" className={classes.sentiment}>Negative</TableCell>
                                <TableCell align="center" className={classes.sentiment}>Neutral</TableCell>
                                <TableCell align="center" className={classes.sentiment}>Positive</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            <TableRow>
                                <TableCell className={classes.firstCol}>
                                    <FastfoodOutlinedIcon className={classes.iconInline}/>
                                    <Typography className={classes.category}
                                    component={"h6"}>Food</Typography>
                                </TableCell>
                                {
                                    resultState.slice(0,4).map(v => {
                                        if (v) {
                                            return <TableCell align="center"><CheckCircleIcon className={classes.checked}/></TableCell>
                                        } else {
                                            return <TableCell/>
                                        }
                                    })
                                }
                            </TableRow>
                            <TableRow>
                                <TableCell className={classes.firstCol}>
                                    <RoomServiceOutlinedIcon className={classes.iconInline}/>
                                    <Typography className={classes.category}
                                        component={"h6"}>Service</Typography>
                                </TableCell>
                                {
                                    resultState.slice(4,8).map(v => {
                                        if (v) {
                                            return <TableCell align="center"><CheckCircleIcon className={classes.checked}/></TableCell>
                                        } else {
                                            return <TableCell/>
                                        }
                                    })
                                }
                            </TableRow>
                            <TableRow>
                                <TableCell className={classes.firstCol}>
                                    <MonetizationOnOutlinedIcon className={classes.iconInline}/>
                                    <Typography className={classes.category}
                                        component={"h6"}>Price</Typography>
                                </TableCell>
                                {
                                    resultState.slice(8, 12).map(v => {
                                        if (v) {
                                            return <TableCell align="center"><CheckCircleIcon className={classes.checked}/></TableCell>
                                        } else {
                                            return <TableCell/>
                                        }
                                    })
                                }
                            </TableRow>
                        </TableBody>
                    </Table>
                </div>

            </Paper> : null}

            <Modal open={openLoading}>
                <Paper className={classes.modal}>
                    <Typography component={"h6"} variant={"h6"} className={classes.wait}>Analyzing...</Typography>
                    <CircularProgress style={{marginLeft: 110, marginTop: 40}} size={80} color={"primary"}/>
                </Paper>
            </Modal>
        </div>
    )
}
