// --- Логика переключателей (уже была ранее) ---
const configs = [
  { id: 'antiBlockBtn', key: 'antiEnabled' },
  { id: 'adBlockBtn', key: 'adBlockEnabled' }
];

configs.forEach(cfg => {
  const btn = document.getElementById(cfg.id);
  chrome.storage.local.get([cfg.key], (res) => updateBtn(btn, res[cfg.key]));
  btn.addEventListener('click', () => {
    chrome.storage.local.get([cfg.key], (res) => {
      const newVal = !res[cfg.key];
      chrome.storage.local.set({ [cfg.key]: newVal }, () => {
        updateBtn(btn, newVal);
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
          if (tabs[0]) chrome.tabs.reload(tabs[0].id);
        });
      });
    });
  });
});

function updateBtn(btn, val) {
  btn.innerText = val ? "ON" : "OFF";
  btn.className = val ? "btn-on" : "btn-off";
}

// --- НОВАЯ ЛОГИКА: Загрузка рекламы из конфига ---
async function loadAds() {
  try {
    // Читаем локальный файл ads.json
    const response = await fetch(chrome.runtime.getURL('ads.json'));
    const data = await response.json();

    const adContainer = document.getElementById('ad-container');
    const adLink = document.getElementById('ad-link');
    const adImg = document.getElementById('ad-img');
    const adText = document.getElementById('ad-text');

    // Заполняем данными
    adLink.href = data.link;
    adImg.src = chrome.runtime.getURL(data.image); // Важно: используем getURL
    adText.innerText = data.text;

    // Показываем блок
    adContainer.style.display = 'block';
  } catch (error) {
    console.error("Ошибка загрузки рекламы:", error);
  }
}

// Запускаем при открытии
loadAds();