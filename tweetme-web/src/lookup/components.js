export function loadTweets(callback) {
    const xhr = new XMLHttpRequest();
    const method = 'GET';
    const url = 'http://localhost:8000/api/tweets/';
    const responseType = 'json';

    xhr.responseType = responseType;
    xhr.open(method, url);
    xhr.onload = function () {
        callback(xhr.response, xhr.status)

    };
    console.log(xhr.response);

    xhr.onerror = function () {
        callback({"message": "There was an error with the request"}, 400)
    };
    xhr.send()
}
