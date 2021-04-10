import {useStyles} from "./Search.styles";
import React, {useEffect} from "react";
import {
    Avatar,
    Button,
    ButtonBase,
    CircularProgress,
    Collapse, Divider,
    Grid,
    InputBase,
    ListItem, ListItemAvatar, ListItemText,
    Paper, Tooltip,
    Typography
} from "@material-ui/core";
import SearchIcon from "@material-ui/icons/Search";
import RestaurantMenuIcon from '@material-ui/icons/RestaurantMenu';
import {ExpandLess, ExpandMore} from "@material-ui/icons";
import AdvancedOption from "./AdvancedOption";
import QueryAPI from "./api/Query.api";
import SortBy from "./SortBy";
import {Switch} from "@material-ui/core";
import {FormControlLabel} from "@material-ui/core";
import TextParserWorker from "./TextParserWorker";

type QueryResponse = {
    _id: string,
    _index: string,
    _score: number,
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

export default function Search() {
    const classes = useStyles();
    const [searchResult, setSearchResult] = React.useState<QueryResponse[]>([]);
    const [collapseId, setCollapseId] = React.useState(new Array(100).fill(true));
    const [loading, setLoading] = React.useState(false);
    const resultCounter = React.useRef(0);
    const queryCounter = React.useRef(1);
    const [queryTerm, setQueryTerm] = React.useState("");
    const [queryTime, setQueryTime] = React.useState(0);
    const [suggestion, setSuggestion] = React.useState("");
    const [switchHighLight, setSwitchHighLight] = React.useState(false);

    // this variable to control the state of the component to avoid mem leak
    const isMounted = React.useRef(true);
    const locationOptions = React.useRef<number[]>([]);
    const sentimentsOptions = React.useRef<number[]>([]);

    useEffect(() => {
        TextParserWorker.subscribeWorker((e: MessageEvent) => {
            setSearchResult(e.data);
        })

        return () => {
            isMounted.current = false;
            TextParserWorker.unsubscribeWorker();
        }
    }, []);

    useEffect(() => {
        textHighlighter(searchResult);
    }, [switchHighLight])


    const openCollapse = (id: number) => {
        setCollapseId(prevState => prevState.map((v, index) => {
            if (index === id) {
                return !v;
            }

            return v;
        }));
    }

    const renderSearchResult = () => {
        let listUserRender: JSX.Element[] = [];

        searchResult.forEach((u, index) => {
            listUserRender.push(
                <div key={u._id}>
                    <ListItem>
                        <ListItemAvatar>
                            <Avatar className={getRatingColor(u._source.rating)}>
                                {/*<Typography variant={"h6"} component={"h6"}>{u._source.rating}</Typography>*/}
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary={
                            <Typography className={collapseId[index] ? classes.reviewFull : classes.reviewCrop}
                                        component={"p"} dangerouslySetInnerHTML={{__html: u._source.review}}>
                            </Typography>
                        } secondary={u._source.username + " | " + u._source.date_inserted}/>
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

        return listUserRender;
    }

    const textHighlighter = (response: QueryResponse[]) => {
        TextParserWorker.postMessage({data: response, queryTerm: queryTerm, mode: switchHighLight ? 1: 0});
    }

    const handleQuery = (defaultTerm?: string) => {
        if (queryTerm.length === 0 && defaultTerm === undefined) {
            return
        }

        if (defaultTerm === undefined) {
            defaultTerm = queryTerm;
        }

        setLoading(true);

        QueryAPI.query(defaultTerm, locationOptions.current, sentimentsOptions.current, queryCounter.current, (res: { status: number, counter: number, time: number, suggesters: any, data: QueryResponse[] }) => {
            if (!isMounted.current) {
                return;
            }

            if (res.counter > resultCounter.current) {
                resultCounter.current = res.counter;
                textHighlighter(res.data);
                setQueryTime(res.time);

                if (res.suggesters.length > 0) {
                    setSuggestion(res.suggesters[0].text);
                } else {
                    setSuggestion("");
                }
            }

            if (resultCounter.current + 1 === queryCounter.current) {
                setLoading(false);
            }
        })

        queryCounter.current += 1;
    }

    const updateAdvancedOptions = (locations: number[], sentiments: number[]) => {
        locationOptions.current = locations;
        sentimentsOptions.current = sentiments;
    }

    const getRatingColor = (rating: number) => {
        if (rating >= 4) {
            return classes.avatarPos;
        } else if (rating === 3) {
            return classes.avatarNeutral;
        }

        return classes.avatarNeg
    }

    const sortResults = (sortType: number) => {
        let resultsCopy = [...searchResult];
        if (sortType === 0) {
            resultsCopy.sort((a, b) => {
                if (a._score > b._score) {
                    return -1;
                }

                return 1
            })
        } else if (sortType === 1) {
            resultsCopy.sort((a, b) => {
                if (a._source.rating > b._source.rating) {
                    return -1;
                }

                return 1
            })
        }

        setSearchResult(resultsCopy);
    }

    const getSuggester = () => {
        setQueryTerm(suggestion);
        handleQuery(suggestion);
    }

    // @ts-ignore
    return (
        <div>
            <div>
                <RestaurantMenuIcon className={`${classes.searchTitle} ${classes.mainIcon}`}/>
                <Typography component={"h6"} variant={"h6"} className={classes.searchTitle}>
                    Find reviews of food, restaurants in Singapore
                </Typography>
            </div>

            <Paper elevation={3} className={classes.search}>
                <div className={classes.searchIcon}>
                    <SearchIcon/>
                </div>
                <InputBase
                    placeholder="Search…"
                    className={classes.inputInput}
                    inputProps={{'aria-label': 'search'}}
                    value={queryTerm}
                    onChange={(e) => {
                        setQueryTerm(e.target.value)
                    }}
                />
                {loading ? <CircularProgress className={classes.circular} size={20}/> : null}
            </Paper>

            <AdvancedOption callback={updateAdvancedOptions}/>

            <Button disabled={queryTerm.length === 0} onClick={() => handleQuery()} variant={'contained'}
                    size={'large'}
                    className={classes.searchBtn}>Search</Button>

            {
                searchResult.length > 0 ?
                    <Paper className={classes.searchResult}>
                        <Grid container>
                            <Grid className={classes.statistics} item xs={6}>
                                <Typography className={classes.queryTime} component={"p"}>Query
                                    time: {queryTime} ms</Typography>
                                {suggestion.length > 0 ?
                                    <Typography style={{fontStyle: "italic"}} component={"p"}>Do you mean <ButtonBase
                                        onClick={getSuggester}><strong style={{
                                        fontSize: 16,
                                        textDecoration: "underline",
                                        fontStyle: "italic"
                                    }}>{suggestion}</strong></ButtonBase> ?</Typography>
                                    : null
                                }
                            </Grid>
                            <Grid item xs={6}>
                                <SortBy callback={sortResults}/>
                                <div className={classes.switchBlock}>
                                    <FormControlLabel
                                        control={<Switch checked={switchHighLight}
                                                         onChange={() => setSwitchHighLight(!switchHighLight)}
                                                         name="switch"/>}
                                        label="Highlight"
                                    />
                                </div>
                            </Grid>
                        </Grid>
                        {renderSearchResult()}
                    </Paper>
                    : null
            }
        </div>
    );
}
