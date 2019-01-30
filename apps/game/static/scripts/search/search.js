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
        const term = encodeURI(event.target.value.replace('#', ''));
        url = `/games/search/search-term?tag=${term}`;
      } else if (event.target.value[0] == '@') {
        const term = encodeURI(event.target.value.replace('@', ''));
        url = `/games/search/search-term?author=${term}`;
      } else {
        const term = encodeURI(event.target.value);
        url = `/games/search/search-term?name=${term}`;
      }
    } else if (check == 'Library') {
      if (event.target.value[0] == '#') {
        const term = encodeURI(event.target.value.replace('#', ''));
        url = `/games/library/search/search-term?tag=${term}`;
      } else if (event.target.value[0] == '@') {
        const term = encodeURI(event.target.value.replace('@', ''));
        url = `/games/library/search/search-term?author=${term}`;
      } else {
        const term = encodeURI(event.target.value);
        url = `/games/library/search/search-term?name=${term}`;
      }
    }

    fetch(url, {
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

  // Execute the auto suggestion
  searchterm.addEventListener('input', function (event) {
    let query = event.target.value;
    if (query.length >= minlength) {
      search(event);
    }
  });

  /* Create the auto-suggestion function */
  function autosuggestion(input, namelist) {
    clearChildren(suggestionList);
    /* The autosuggestion function takes two arguments, the input value and a list of possible autosuggested values */
    // Create currentFocus to define the position of suggested item to add class active and simulate a click event
    let currentFocus;
    // someone input a search
    let val = input.value;
    // Close all already opened suggestions of a search
    if (!val) { return false; }
    currentFocus = -1;
    // For each item in the array, if the item is the same with the value
    // in the input, it will create a new div element for each maching item
    namelist.forEach(function (item) {
      if (item.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        // Create a DIV element for each matching item
        newdiv2 = document.createElement('div');
        // Add the name to the div
        // Check if the search for category, developer or game name
        if (val[0] == '@') {
          newdiv2.innerHTML = 'Search for developer ' + item;
        } else if (val[0] == '#') {
          newdiv2.innerHTML = 'Search for category ' + item;
        } else {
          newdiv2.innerHTML = 'Search for game: ' + item;
        }
        // Insert a input field that will hold the current array item's value
        newdiv2.innerHTML += `<input type='hidden' value='${item}'>`;
        // Execute a function when someone clicks on the item value (DIV element)
        newdiv2.addEventListener('click', function (e) {
          // Insert the value for the search input field
          input.value = e.target.getElementsByTagName('input')[0].value;
          // Close all already opened suggestions of a search
          closeSuggestion();
          // Submit the form
          searchBtn.click();
        });
        newdiv1.appendChild(newdiv2);
      }
    })
    
    // Execute a function which handle key press in the keyboard
    input.addEventListener('keydown', function (evt) {
      let selectedItem = document.getElementById('autosuggestionListItem');
      if (selectedItem) {
        selectedItem = selectedItem.getElementsByTagName('div');
      }
      if (evt.keyCode == 40) {
        // Increase the currentFocus as the arrow DOWN key is pressed
        currentFocus += 1;
        // Add class active to the selected item
        addActive(selectedItem);
      } else if (evt.keyCode == 38) {
        // Decrease the currentFocus as the arrow UP key is pressed
        currentFocus -= 1;
        // Add class active to the selected item
        addActive(selectedItem);
      } else if (evt.keyCode == 13) {
        // The ENTER key is pressed
        evt.preventDefault();
        if (currentFocus > -1) {
          // Simulate a click on the active item
          if (selectedItem) {
            selectedItem[currentFocus].click();
          }
        } else {
          // Submit the form
          searchBtn.click();
        }
      }
    });

    // Create function used to clear suggestion list
    function clearChildren(element) {
      while (element.firstChild) {
        element.removeChild(element.firstChild)
      }
    }
    // Create function to add active class to the item
    function addActive(items) {
      if (!items) {
        return false;
      }
      // Removing class active on all items
      removeActive(items);
      if (currentFocus >= items.length) {
        currentFocus = 0;
      }
      if (currentFocus < 0) {
        currentFocus = items.length - 1;
      }
      // Add class active to current focus item
      items[currentFocus].classList.add('autosuggestion-active');
    }

    // Create function to remove active class from all items
    function removeActive(items) {
      for (let i = 0; i < items.length; i++) {
        items[i].classList.remove('autosuggestion-active');
      }
    }

    // Close all the suggestion list when someone clicks in the document except clicking on the suggestion list itself
    document.addEventListener('click', function (e) {
      closeSuggestion(e.target);
    });
  }
})()
