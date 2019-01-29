window.getCookie = window.getCookie || function (name) {
  var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) {
    return match[2];
  }
}

const defaultOptions = {
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

const defaultFetch = (
  url = "",
  data = {},
  {method = "POST", ...options} = {method: "POST"}
) => {
  args = {
    ...defaultOptions,
    ...options,
    method,
    body: JSON.stringify(data),
  };
  return fetch(
    encodeURI(url),
    args,
  )
};
