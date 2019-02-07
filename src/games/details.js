/* global gameID */
import {defaultFetch} from '../util.js';

(() => {
  const deleteReviewBtn = document.getElementById('delete-review');
  const deleteGameBtn = document.getElementById('delete-game');

  const onReviewDelete = (e) => {
    defaultFetch(
        `/games/${gameID}/review/delete/`,
        undefined, {method: 'DELETE'}
    )
        .then((response) => response.json())
        .then((response) => {
          if (response.message == 'success') {
            deleteReviewBtn.parentNode.parentNode.remove();
          } else {
            deleteReviewBtn.innerText = response.message;
            deleteReviewBtn.classList.add('disabled');
            deleteReviewBtn.removeEventListener('click', onReviewDelete);
          }
        });
  };

  const onGameDelete = (e) => {
    if (window.confirm('are you sure you want to delete the game? The operation cannot be cancelled')) {
      defaultFetch(
          `/games/${gameID}/edit/`,
          undefined,
          {method: 'DELETE'}
      )
          .then((response) => {
            if (response.ok) {
              window.location.href = '/games/uploads/';
            }
          });
    }
  };

  if (deleteReviewBtn) {
    deleteReviewBtn.addEventListener('click', onReviewDelete);
  }
  if (deleteGameBtn) {
    deleteGameBtn.addEventListener('click', onGameDelete);
  }
})();
