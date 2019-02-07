import {defaultFetch} from './util.js';

(() => {
  const becomeDeveloper = document.getElementById('become-developer');
  const isDeveloper = !becomeDeveloper;

  if (isDeveloper) {
    const generateBtn = document.getElementById('generate-key');
    const input = document.getElementById('id-apikey');
    const copyBtn = document.getElementById('copy');
    const onGenerateClick = (e) => {
      defaultFetch('/api/v1/generate/')
          .then((response) => response.json())
          .then((response) => {
            input.value = response.message;
          });
    };

    const onCopyClick = (e) => {
      input.select();
      document.execCommand('copy');
      window.alert('Api key copied to clipboard.');
    };

    generateBtn.addEventListener('click', onGenerateClick);
    copyBtn.addEventListener('click', onCopyClick);

    return;
  }
})();
