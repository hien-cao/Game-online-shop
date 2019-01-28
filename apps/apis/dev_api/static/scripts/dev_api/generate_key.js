(() => {
  const generateBtn = document.getElementById("generate_key");
  const input = document.getElementById("id_apikey");
  const copyBtn = document.getElementById("copy");

  const onGenerateClick = (e) => {
    postData("/api/v1/generate")
      .then(response => response.json())
      .then(response => {
        input.value = response.message;
      });
  }

  const onCopyClick = (e) => {
    input.select();
    document.execCommand("copy");
    window.alert("Api key copied to clipboard.");
  }

  const addEventListeners = () => {
    generateBtn.addEventListener("click", onGenerateClick);
    copyBtn.addEventListener("click", onCopyClick);
  }

  addEventListeners();
})();
