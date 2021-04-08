const htmlregex = /(<([^>]+)>)/ig;
const fields = ['review', 'location', 'name'];
const mode = Object.freeze({highlight: 1, normal: 0});

const stripTag = (e) => {
    let data = e.data.data;

    for (let i = 0; i < data.length; i++) {
        for (let f = 0; f < 3; f++) {
            data[i]._source[fields[f]] = data[i]._source[fields[f]].replace(htmlregex, "");
        }
    }

    return data;
}

function customSort(a, b) {
    if (a[0] < b[0]) {
        return -1
    } else if (a[0] > b[0]) {
        return 1
    }

    if (a[1] < b[1]) {
        return -1;
    } else if (a[1] > b[1]) {
        return 1;
    }

    return 0
}

const highlightText = (e) => {
    let queryTerm = e.data.queryTerm;
    let data = e.data.data;
    let tokens = queryTerm.split(" ").map(e => e.toLowerCase());

    for (let i = 0; i < data.length; i++) {
        for (let f = 0; f < 3; f++) {
            let text = data[i]._source[fields[f]].replace(htmlregex, "");
            let arr = [];
            for (let q = 0; q < tokens.length; q++) {
                let re = new RegExp(tokens[q], 'gi');

                let match = [];
                while ((match = re.exec(text)) != null) {
                    arr.push([match.index, match.index + tokens[q].length]);
                }
            }

            if (arr.length === 0) {
                continue
            }

            let processed = "";
            let cur = 0;
            let index, end;

            // process the string from left to right
            arr.sort(customSort);

            let intervals = [];
            let start = arr[0][0];
            let furthest = arr[0][1];

            for (let p = 1; p < arr.length; p ++) {
                if (arr[p][0] < furthest) {
                    furthest = arr[p][1];
                    continue;
                }

                intervals.push([start, furthest]);
                start = arr[p][0];
                furthest = arr[p][1];
            }

            intervals.push([start, furthest]);
            intervals.sort(customSort);

            intervals.forEach(element => {
                index = element[0];
                end = element[1];
                processed += text.slice(cur, index) + "<span class='highlighter'>" + text.slice(index, end) + "</span>";
                cur = end;
            })

            processed += text.slice(cur);
            data[i]._source[fields[f]] = processed
        }
    }

    return data;
}

onmessage = (e) => {
    if (e.data.mode === mode.highlight) {
        postMessage(highlightText(e));
    } else {
        postMessage(stripTag(e))
    }
};

