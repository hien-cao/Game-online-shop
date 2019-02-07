import {defaultFetch} from '../util.js';

(() => {
  const deleteReviewBtn = document.getElementById("delete_review");
  const onDeleteClick = (e) => {
    defaultFetch(`/games/${gameID}/review/delete/`, undefined, {method: "DELETE"})
      .then(response => response.json())
      .then(response => {
        if (response.message == "success") {
          deleteReviewBtn.parentNode.parentNode.remove();
        } else {
          deleteReviewBtn.innerText = response.message;
          deleteReviewBtn.classList.add("disabled");
          deteleReviewBtn.removeEventListener("click", onDeleteClick);
        }
      });
  };

  deleteReviewBtn.addEventListener("click", onDeleteClick)
})();
