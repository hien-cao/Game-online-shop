// helper function to parse document cookie
export const parseCookie = (name) => {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) {
    return match[2];
  }
};

const defaultOptions = {
  method: 'POST',
  mode: 'cors',
  cache: 'no-cache',
  credentials: 'same-origin',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': parseCookie('csrftoken'),
  },
  redirect: 'follow',
  referrer: 'no-referrer',
};

export const defaultFetch = (
    url = '',
    data = {},
    {method = 'POST', ...options} = {method: 'POST'}
) => {
  return fetch(
      encodeURI(url),
      {
        ...defaultOptions,
        ...options,
        method,
        body: JSON.stringify(data),
      }
  );
};
