// Inject the shared header and footer, then wire up the bits that depend on them.

function highlightCurrentSection() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav a').forEach(link => {
    const section = new URL(link.href, window.location.origin).pathname;
    if (section !== '/' && path.startsWith(section)) {
      link.setAttribute('aria-current', 'page');
    }
  });
}

function stampCurrentYear() {
  const el = document.getElementById('current-year');
  if (el) el.textContent = new Date().getFullYear();
}

function inject(targetId, url, done) {
  const target = document.getElementById(targetId);
  if (!target) return;
  fetch(url)
    .then(response => response.text())
    .then(html => {
      target.innerHTML = html;
      if (done) done();
    })
    .catch(() => { /* leave the slot empty rather than breaking the page */ });
}

inject('header', '/header.html', highlightCurrentSection);
inject('footer', '/footer.html', stampCurrentYear);
