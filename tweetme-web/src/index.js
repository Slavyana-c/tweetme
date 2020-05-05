import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {FeedComponent, TweetsComponent, TweetDetailComponent} from "./tweets";

const appEl = document.getElementById('root');
if(appEl) {
    ReactDOM.render(<App/>, appEl);
}

// this way we pass all dataset elements to props, not just 1 by 1
const e = React.createElement;
const tweetsEl = document.getElementById('tweetme');
if(tweetsEl) {
    ReactDOM.render(e(TweetsComponent, tweetsEl.dataset), tweetsEl);
}

const tweetFeedEl  = document.getElementById('tweetme-feed');
if(tweetsEl) {
    ReactDOM.render(e(FeedComponent, tweetFeedEl.dataset), tweetFeedEl);
}

const tweetDetailElements = document.querySelectorAll(".tweetme-detail");
tweetDetailElements.forEach(container => {
         ReactDOM.render(e(TweetDetailComponent, container.dataset), container);

});

// ReactDOM.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
//   document.getElementById('root')
// );

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
