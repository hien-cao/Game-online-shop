(() => {
  const btn = document.getElementById("generate_key");
  const input = document.getElementById("id_apikey");

  const onClick = (e) => {
    postData("/api/v1/generate")
      .then(response => response.json())
      .then(response => {
        input.value = response.message;
      });
  }

  const addEventListeners = () => {
    btn.addEventListener('click', onClick);
  }

  addEventListeners();
})();
