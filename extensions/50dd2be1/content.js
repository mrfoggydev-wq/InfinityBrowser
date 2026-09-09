chrome.storage.local.get(['enabled'], (result) => {
  if (result.enabled) {
    console.log("Anti-Block активен");
    
    const fixAds = () => {
      // Ищем элементы, которые часто скрывают блокировщики
      const selectors = ['[class*="ad-"]', '.adsbygoogle', '#banner'];
      selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
          el.style.setProperty('display', 'block', 'important');
          el.style.setProperty('visibility', 'visible', 'important');
          el.style.setProperty('opacity', '1', 'important');
        });
      });
    };

    // Следим за динамическим контентом
    const observer = new MutationObserver(fixAds);
    observer.observe(document.body, { childList: true, subtree: true });
    
    fixAds();
  }
});