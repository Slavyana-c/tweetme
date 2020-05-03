import React, {useState} from "react";
import {apiTweetCreate} from "./lookup";
import {TweetsList} from "./list";
import {TweetCreate} from "./create";

export function TweetsComponent(props) {
    const textAreaRef = React.createRef();

    const [newTweets, setNewTweets] = useState([]);

    const canTweet = props.canTweet === 'false' ? false : true

    const handleBackendUpdate = (response, status) => {
        // backend api response handler
        let tempNewTweets = [...newTweets];
        tempNewTweets.unshift(response);
        setNewTweets(tempNewTweets)
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        const newVal = textAreaRef.current.value;

        // backend api request
        apiTweetCreate(newVal, handleBackendUpdate);

        textAreaRef.current.value = ' '
    };

    return <div className={props.className}>
        {canTweet === true &&
        <TweetCreate didTweet={handleBackendUpdate} className={'col-12 mb-3'}/>}
        {/*pass all props from this component*/}
        <TweetsList newTweets={newTweets} {...props}/>

    </div>
}

