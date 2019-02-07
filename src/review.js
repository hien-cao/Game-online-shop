(() => {
  const gradeInput = document.getElementById('id_grade');
  const circleElems = document.getElementsByClassName('circle');

  const onCircleClick = (e) => {
    const {
      target: {
        id,
      },
    } = e;
    const value = id.slice(-1);
    gradeInput.value = value;
    colorize(value);
  };

  const colorize = (value) => {
    for (const circleElem of circleElems) {
      const circleVal = circleElem.id.slice(-1);
      if (circleVal <= value) {
        circleElem.classList.add('full');
      } else {
        circleElem.classList.remove('full');
      }
    }
  };

  for (const circleElem of circleElems) {
    circleElem.addEventListener('click', onCircleClick);
  }

  colorize(gradeInput.value);
})();
