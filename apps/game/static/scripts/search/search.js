'use strict';
/*
    The search.js handles the search engine for the games in the web app. The game can be sought by name, categories, and developer name. The suggestions  are provided based on the current input in the search box.
    In order to use the search, follow the below instructions:
      + Start with "@" to search for games with the desired developer
      + Start with "#" to search for games with the desired categories tags
      + Start with no prefix to search for games with the desired name
  */
(() => {
  // Check if the search from page browse or library
  let check = document.querySelector('.is-active').textContent.trim();

  const debounced = function (fn, delay) {
    let timeout;
    return function () {
      clearTimeout(timeout)
      timeout = setTimeout(() => fn(...arguments), delay);
    };
  };

  const search = debounced((event) => {
    let url;
    if (check == 'Browse') {
      if (event.target.value[0] == '#') {
        const term = event.target.value.replace('#', '');
        url = `/games/search/search-term?tag=${term}`;
      } else if (event.target.value[0] == '@') {
        const term = event.target.value.replace('@', '');
        url = `/games/search/search-term?author=${term}`;
      } else {
        const term = event.target.value;
        url = `/games/search/search-term?name=${term}`;
      }
    } else if (check == 'Library') {
      if (event.target.value[0] == '#') {
        const term = event.target.value.replace('#', '');
        url = `/games/library/search/search-term?tag=${term}`;
      } else if (event.target.value[0] == '@') {
        const term = event.target.value.replace('@', '');
        url = `/games/library/search/search-term?author=${term}`;
      } else {
        const term = event.target.value;
        url = `/games/library/search/search-term?name=${term}`;
      }
    }

    fetch(encodeURI(url), {
      method: 'GET',
    })
      .then(response => response.json())
      .then(data => autosuggestion(event.target, data.results))
      .catch(error => console.error(error))
  }, 300);

  /* Define the variable */
  const searchForm = document.getElementById('search-form');
  const suggestionList = document.getElementById('suggestion-list');
  const searchterm = document.getElementById('searchterm');
  const searchBtn = document.getElementById('search_btn');
  const minlength = 2;

  // Execute a function which handle key press in the keyboard
  searchterm.addEventListener('keydown', function (evt) {
    if (evt.keyCode == 40) {
      // Increase the currentFocus as the arrow DOWN key is pressed
      currentFocus += 1;
    } else if (evt.keyCode == 38) {
      // Decrease the currentFocus as the arrow UP key is pressed
      currentFocus -= 1;
    } else if (evt.keyCode == 13) {
      // The ENTER key is pressed
      evt.preventDefault();
      if (currentFocus > -1) {
        // Simulate a click on the active item
        if (suggestionList) {
          suggestionList.children[currentFocus].click();
        }
      } else {
        // Submit the form
        searchBtn.click();
      }
      return; // if enter was pressed, no need to invoke setAsActive.
    }
    if (currentFocus >= suggestionList.children.length) {
      currentFocus = 0;
    }
    if (currentFocus < 0) {
      currentFocus = suggestionList.children.length - 1;
    }
    // Add class active to the selected item
    setAsActive(suggestionList.children);
  });


  // Execute the auto suggestion
  searchterm.addEventListener('input', function (event) {
    let query = event.target.value;
    if (query.length >= minlength) {
      search(event);
    }
  });

  /* Create the auto-suggestion function */
  function autosuggestion(query, namelist) {
    clearChildren(suggestionList);
    /* The autosuggestion function takes two arguments, the input value and a list of possible autosuggested values */
    // Create currentFocus to define the position of suggested item to add class active and simulate a click event
    // Close all already opened suggestions of a search
    if (!val) { return false; }
    currentFocus = -1;
    // For each item in the array, if the item is the same with the value
    // in the input, it will create a new div element for each maching item
    namelist.forEach(function (item) {
      if (item.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        // Create a DIV element for each matching item
        const suggestionContainer = document.createElement('div');
        // Add the name to the div
        // Check if the search for category, developer or game name
        if (val[0] == '@') {
          suggestionContainer.innerHTML = 'Search by developer ' + item;
        } else if (val[0] == '#') {
          suggestionContainer.innerHTML = 'Search by category ' + item;
        } else {
          suggestionContainer.innerHTML = item;
        }
        // Execute a function when someone clicks on the item value (DIV element)
        suggestionContainer.addEventListener('click', function (e) {
          search(item);
        });
        suggestionList.appendChild(suggestionContainer);
      }
    })

    // Create function used to clear suggestion list
    function clearChildren(element) {
      while (element.firstChild) {
        element.removeChild(element.firstChild)
      }
    }
    // Create function to add active class to the item
    function setAsActive(suggestionElements = []) {
      if (suggestionElements.length == 0) {
        return false;
      }
      // Removing class active on all suggestionElements
      for (let i = 0; i < suggestionElements.length; i++) {
        if (i == currentFocus) {
          // Add class active to current focus item
          suggestionElements[currentFocus].classList.add('suggestion-active');
          continue;
        }
        suggestionElements[i].classList.remove('suggestion-active');
      }
    }

    function isNestedElement(parent, element) {
        for (const child of parent.children) {
          if (child == element || isNestedElement(child, element)) {
            return true
          }
        }
        return false;
    }
    // Close all the suggestion list when someone clicks in the document except clicking on the suggestion list itself
    document.addEventListener('click', function (e) {
      if (!isNestedElement(searchForm, e.target)) {
        clearChildren(suggestionList);
      }
    });
  }
})()
