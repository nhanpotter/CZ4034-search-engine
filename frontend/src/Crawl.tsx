import {
    Avatar,
    Button,
    CircularProgress, Collapse, Divider,
    InputBase,
    ListItem,
    ListItemAvatar, ListItemText,
    Modal,
    Paper, Tooltip,
    Typography
} from "@material-ui/core";
import SearchIcon from "@material-ui/icons/Search";
import React from "react";
import Alert from '@material-ui/lab/Alert';
import YoutubeSearchedForOutlinedIcon from '@material-ui/icons/YoutubeSearchedForOutlined';
import {useStyles} from './Crawl.styles';
import QueryAPI from "./api/Query.api";
import {ExpandLess, ExpandMore} from "@material-ui/icons";

enum alertType {error = 'error', success = 'success'};

type CrawlResponse = {
    _index: string,
    _source: {
        date_inserted: string,
        location: string,
        name: string,
        rating: number,
        res_id: number,
        review: string,
        username: string
    }
}

export default function Crawl() {
    const classes = useStyles();
    const [inputURL, setInputURL] = React.useState("");
    const [numberInput, setNumberInput] = React.useState<any>("");
    const [openLoading, setOpenLoading] = React.useState(false);
    const [alertStatus, setAlertStatus] = React.useState<alertType | undefined>(undefined);
    const [alertInfo, setAlertInfo] = React.useState("");
    const [crawlResult, setCrawlResult] = React.useState<CrawlResponse[]>([]);
    const [collapseId, setCollapseId] = React.useState(new Array(100).fill(false));

    const changeNumberInput = (value: any) => {
        if (!isNaN(value)) {
            let num = parseInt(value);
            if (num > 50) {
                num = 50;
            } else if (num <= 0) {
                num = 1
            }

            setNumberInput(num);
        }
    }

    const openCollapse = (id: number) => {
        setCollapseId(prevState => prevState.map((v, index) => {
            if (index === id) {
                return !v;
            }

            return v;
        }));
    }

    const handleCrawl = () => {
        if (!numberInput || !inputURL) {
            return;
        }

        setOpenLoading(true);
        QueryAPI.crawl(inputURL, numberInput, (res: any) => {
            if (res.status === 1 && res.data.errors === undefined) {
                setAlertInfo("The reviews are successfully crawled")
                setAlertStatus(alertType.success);
                setCrawlResult(res.data.data);
            } else if (res.status === 1) {
                setAlertInfo(res.data.errors);
                setAlertStatus(alertType.error);
                setCrawlResult([]);
            }

            setOpenLoading(false);
        })
    }

    const getRatingColor = (rating: number) => {
        if (rating >= 4) {
            return classes.avatarPos;
        } else if (rating === 3) {
            return classes.avatarNeutral;
        }

        return classes.avatarNeg
    }

    const renderCrawlResult = (): JSX.Element[] => {
        let renderArr: JSX.Element[] = [];

        crawlResult.forEach((u, index) => {
            renderArr.push(
                <div key={index + "__crawl"}>
                    <ListItem>
                        <ListItemAvatar>
                            <Tooltip title={"User Rating"}>
                                <Avatar className={getRatingColor(u._source.rating)}>
                                    <Typography variant={"h6"} component={"h6"}>{u._source.rating}</Typography>
                                </Avatar>
                            </Tooltip>
                        </ListItemAvatar>
                        <ListItemText primary={
                            <Typography className={collapseId[index] ? classes.reviewFull : classes.reviewCrop}
                                        component={"p"}>
                                {u._source.review}
                            </Typography>
                        } secondary={u._source.date_inserted}/>
                        <div onClick={() => openCollapse(index)}>
                            {collapseId[index] ? <ExpandLess/> : <ExpandMore/>}
                        </div>
                    </ListItem>

                    <Collapse className={classes.clps} in={collapseId[index]} unmountOnExit>
                        <Typography component={"h6"} variant={"h6"} className={classes.infoTitle}
                                    dangerouslySetInnerHTML={{__html: u._source.name}}/>
                        <Typography className={classes.infoDetail}
                                    dangerouslySetInnerHTML={{__html: "Address: " + u._source.location}}/>
                    </Collapse>
                    <Divider className={classes.divider} variant="inset"/>
                </div>
            )
        })

        return renderArr;
    }

    return (
        <div>
            <div>
                <YoutubeSearchedForOutlinedIcon className={`${classes.searchTitle} ${classes.mainIcon}`}/>
                <Typography component={"h6"} variant={"h6"} className={classes.searchTitle}>
                    Crawl reviews of restaurants from Trip Advisor
                </Typography>
            </div>

            <Paper elevation={3} className={classes.search}>
                <div className={classes.searchIcon}>
                    <SearchIcon/>
                </div>
                <InputBase
                    placeholder="URL..."
                    className={classes.inputInput}
                    inputProps={{'aria-label': 'search'}}
                    value={inputURL}
                    onChange={(e) => {
                        setInputURL(e.target.value)
                    }}
                />

                <InputBase
                    value={numberInput}
                    onChange={(e) => {
                        changeNumberInput(e.target.value)
                    }}
                    type={"number"} className={classes.inputNumber} placeholder={"Number of reviews"}/>
            </Paper>

            {alertStatus && <Alert className={classes.alert} severity={alertStatus} onClose={() => {
                setAlertStatus(undefined)
            }}>{alertInfo}</Alert>}

            <Button disabled={inputURL.length === 0 || !numberInput} onClick={() => handleCrawl()} variant={'contained'}
                    size={'large'}
                    className={classes.searchBtn}>Crawl</Button>

            <Paper elevation={3} className={classes.guide}>
                <Typography className={classes.boxLabel} component={"h5"} variant={"h5"}> Guideline</Typography>
                <div className={classes.guideInfo}>
                    <Typography component={"p"}>
                        The reviews of restaurants are crawled from TripAdvisor website. Please find the restaurant on
                        Trip Advisor and paste the url to the above input bar. For example, <a
                        href={"https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d13152787-Reviews-Positano_Risto-Singapore.html"}>https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d13152787-Reviews-Positano_Risto-Singapore.html</a> is
                        a valid url.
                    </Typography>

                    <div style={{marginTop: 10}}>
                        <Typography><strong>Note:</strong></Typography>
                        <Typography component={"p"}>
                            &bull; The crawling logic may take long time to complete (10 reviews are estimated to completed
                            in 15 seconds).
                        </Typography>
                        <Typography component={"p"}>
                            &bull; An acceptable range for number of reviews is between 1-50.
                        </Typography>
                        <Typography component={"p"}>
                            &bull; One restaurant can only be crawled <strong>one</strong> time.
                        </Typography>
                    </div>
                </div>
            </Paper>

            {crawlResult ?
                <Paper className={classes.searchResult}>
                    {renderCrawlResult()}
                </Paper>
                : null
            }

            <Modal open={openLoading}>
                <Paper className={classes.modal}>
                    <Typography component={"h6"} variant={"h6"} className={classes.wait}>Please
                        wait...</Typography>
                    <CircularProgress style={{marginLeft: 110, marginTop: 40}} size={80} color={"primary"}/>
                </Paper>
            </Modal>
        </div>
    )
}
