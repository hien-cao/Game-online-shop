/* 
    The search.js handles the search engine for the games in the web app. The game can be sought by name, categories, and developer name. The suggestions  are provided based on the current input in the search box.
    In order to use the search, follow the below instructions:
      + Start with "@" to search for games with the desired developer
      + Start with "#" to search for games with the desired categories tags
      + Start with no prefix to search for games with the desired name
  */

/* Loading once the document ready */
window.onload = function () {
  'use strict';

  const searchTerm = document.querySelector('.searchTerm');
  const searchBtn = document.querySelector('.searchBtn');

  // Execute the auto suggestion 
  searchTerm.addEventListener('input', function (e) {

    let url = '/' + searchTerm.value;

    fetch(url)
      .then(response => autosuggestion(e, response))
      .catch(error => console.error(error))
  });

  // Execute the search form:
  searchBtn.addEventListener('click', function (e) {
    // Prevent the page reload
    e.preventDefault();
    // Submit the query
    submitSearchForm();
  });

  function submitSearchForm() {
    const data = {
      'query': searchTerm.value
    };
    fetch('/search/', {
      method: 'POST',
      mode: "same-origin",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: data
    })
      .then(response => response.json())
      .catch(error => console.error(error));
  }

  /* Create the auto-suggestion function */
  function autosuggestion(input, nameList) {
    /* The autosuggestion function takes two arguments, the input value and a list of possible autosuggested values */
    // Create currentFocus to define the position of suggested item to add class active and simulate a click event
    let currentFocus;
    // someone input a search
    let newDIV1, newDIV2, val = input.value;
    // Close all already opened suggestions of a search
    closeSuggestion();
    if (!val) { return false; }
    currentFocus = -1;
    // Create a DIV element containing the suggestion name
    newDIV1 = document.createElement('div');
    newDIV1.setAttribute('id', 'autosuggestionListItem');
    newDIV1.setAttribute('class', 'suggestionList');
    // Append The DIV element as a child in the 'autosuggestion' container
    input.parentNode.appendChild(newDIV1);
    // For each item in the array, if the item is the same with the value 
    // in the input, it will create a new div element for each maching item
    nameList.forEach(function (item) {
      if (item.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        // Create a DIV element for each matching item
        newDIV2 = document.createElement('div');
        // Add the name to the div 
        // Check if the search for category, developer or game name
        if (val[0] == '@') {
          newDIV2.innerHTML = 'Search for developer @' + item;
        } else if (val[0] == '#') {
          newDIV2.innerHTML = 'Search for catelogry #' + item;
        } else {
          newDIV2.innerHTML = 'Search for game: ' + item;
        }
        // Insert a input field that will hold the current array item's value
        newDIV2.innerHTML += `<input type='hidden' value='${item}'>`;
        // Execute a function when someone clicks on the item value (DIV element)
        newDIV2.addEventListener('click', function () {
          // Insert the value for the search input field
          input.value = input.getElementsByTagName('input')[0].value;
          // Close all already opened suggestions of a search
          closeSuggestion();
        });
        newDIV1.appendChild(newDIV2);
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
        }
      }
    });

    // Create function to close all suggestion list
    function closeSuggestion(element) {
      // Close suggestion list in the document except the one mentioned in the parameter
      const suggestions = document.getElementsByClassName("suggestionList");
      for (var i = 0; i < suggestions.length; i++) {
        if (element != suggestions[i] && element != input) {
          suggestions[i].parentNode.removeChild(suggestions[i]);
        }
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
}




