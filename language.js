const languageLink = document.querySelector('[data-language]');

if (languageLink) {
  const otherLanguage = new URL(languageLink.href);

  function syncSection() {
    otherLanguage.hash = window.location.hash;
    languageLink.href = otherLanguage.href;
  }

  window.addEventListener('hashchange', syncSection);
  syncSection();
}
