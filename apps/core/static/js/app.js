window.getCookie = window.getCookie || function (name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
        return match[2];
    }
}

const defaultOptions = {
    POST: {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.getCookie("csrftoken"),
        },
        redirect: "follow",
        referrer: "no-referrer",
    }
}

const postData = (url = "", data = {}, options = {}) => {
    args = {
        ...defaultOptions.POST,
        ...options,
        body: JSON.stringify(data),
    };
    return fetch(
        url,
        args,
    )
    .then(response => response.json()); // parses response to JSON
};
