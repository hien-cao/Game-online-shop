const nth = (n) => 5 - n;
const pluckValue = (id) => id[id.length - 1];

(() => {
  const gradeInput = document.getElementById("id_grade");
  const circleElems = document.getElementsByClassName("circle");

  const onCircleClick = (e) => {
    const {
      target: {
        id,
      }
    } = e;
    const value = pluckValue(id);
    gradeInput.value = value;
    colorize(value);
  }

  const colorize = (value) => {
    for (let circleElem of circleElems) {
      const circleVal = pluckValue(circleElem.id);
      if (circleVal <= value) {
        circleElems[nth(circleVal)].classList.add("full");
      } else {
        circleElems[nth(circleVal)].classList.remove("full");
      }
    }
  }

  const addEventListeners = () => {
    for (let circleElem of circleElems) {
      circleElem.addEventListener("click", onCircleClick)
    }
  }


  colorize(gradeInput.value);
  addEventListeners();
})();
