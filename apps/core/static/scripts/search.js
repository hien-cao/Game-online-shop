/* 
    The search.js handles the search engine for the games in the web app. The game can be sought by name, categories, and developer name. The suggestions  are provided based on the current input in the search box.
    In order to use the search, follow the below instructions:
      + Start non-prefix to search for games the desired name
      + Start with "@" to search for games with the desired developer
      + Start with "#" to search for games with the desired categories tags
  */
window.onload = function () {

}
// Create a variables to store the games database
// from game/models/game import Game
// games = Game.objects.all()
const games = []; // List of games json file
const names = []; // List of all games' name
const developers = []; // List of all developers
const tags = []; // List of all categories

// Fetch the data from django view, and report any errors that occur in the fetching processs
fetch({{games_data}}).then(function(response) {
  return response.json();
}).then(function(data) {
  games = data;
  // Execute the main function
  main();
}).catch(function(err) {
  console.log('Errors occur with message: ' + err.message);
})

// Create the main function to contain the logic for the search
function main() {
  // Define the variables in DOM to manipulate the data
  const searchTerm = document.getElementById('searchInput');
  const searchBtn = document.getElementById('searchBtn');
  const gameContainer = document.getElementById('gameContainer');

  // Define the search term for the developer and catelogies
  let lastSearch = '';
  let lastDeveloper = '';
  let lastCatagory = '';
  // The finalGroup contain the games after filtered by search, developer, catagory
  let developerGroup;
  let categoryGroup;
  let finalGroup;

  // As the page loading, all the game will be displayed in order of added date
  finalGroup = games;
  updateDisplay();

  // Empty all groups before the search
  emptyGroup()
  function emptyGroup() {
    developerGroup = [];
    categoryGroup = [];
    finalGroup = [];
  }

  // Function to assign the search value to variables
  function assignTerm() {
    if (searchTerm) {
      searchArray = searchTerm.split(' ');
      searchArray.forEach(function(item) {
        if (item[0] == '@') {
          lastDeveloper = item.slice(1, item.length - 1);
        } else if (item[0] == '#') {
          lastCatagory = item.slice(1, item.length - 1);
        } else {
          lastSearch = item;
        }
      })
    }
  }

  // when the search button is click evoke the developer search
  searchBtn.addEventListener('click', developerSelect)

  // Create the developerSelect to filter game with developer name and add to developerGroup and evoke categorySelect
  function developerSelect() {
    // Assign the search term into search, catagory, and 
    assignTerm();
    // Evoke category search 
    categorySelect();
  }

   // Create the categorySelect to filter game with developer name and add to developerGroup and evoke gameSelect
   function categorySelect() {
     gameSelect()
   }

   // Create a function to update the display of the game with finalGroup of games
   function updateDisplay() {

   }



  /* Create the auto-suggestion function */
  function autosuggestion(input, nameList) {
    /* The autosuggestion function takes two arguments, the input value and a list of possible autosuggested values */
    // Create currentFocus to define the position of suggested item to add class active and simulate a click event
    let currentFocus;
    // Execute a function as someone input a search
    input.addEventListener('input', function () {
      let newDIV1, newDIV2, val = this.value;
      // Close all already opened suggestions of a search
      closeSuggestion();
      if (!val) { return false; }
      currentFocus = -1;
      // Create a DIV element containing the suggestion name
      newDIV1 = document.createElement('div');
      newDIV1.setAttribute('id', 'autosuggestionListItem');
      newDIV1.setAttribute('class', 'suggestionList');
      // Append The DIV element as a child in the 'autosuggestion' container
      this.parentNode.appendChild(newDIV1);
      // For each item in the array, if the item is the same with the value 
      // in the input, it will create a new div element for each maching item
      nameList.forEach(function (item) {
        if (item.substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          // Create a DIV element for each matching item
          newDIV2 = document.createElement('div');
          // Make the maching letters bold
          newDIV2.innerHTML = item;
          // Insert a input field that will hold the current array item's value
          newDIV2.innerHTML += `<input type='hidden' value='${item}'>`;
          // Execute a function when someone clicks on the item value (DIV element)
          newDIV2.addEventListener('click', function () {
            // Insert the value for the search input field
            input.value = this.getElementsByTagName('input')[0].value;
            // Close all already opened suggestions of a search
            closeSuggestion();
          });
          newDIV1.appendChild(newDIV2);
        }
      })
    });
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
    function closeSuggestion(elemnt) {
      // Close suggestion list in the document except the one mentioned in the parameter
      const suggestions = document.getElementsByClassName("suggestionList");
      for (var i = 0; i < suggestions.length; i++) {
        if (elemnt != suggestions[i] && elemnt != input) {
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
    document.addEventListener('click', function (evt) {
      closeSuggestion(evt.target);
    });
  }

  // Execute auto-suggestion function 
  autosuggestion(document.getElementById('searchInput'), gameGroup);
}

