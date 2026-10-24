(() => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const symbols = {
    bookmark: '<path d="M6 4h12v17l-6-4-6 4z"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    moon: '<path d="M20 14A8 8 0 0 1 10 4 8.5 8.5 0 1 0 20 14Z"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
  };
  const icon = name => `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">${symbols[name]}</svg>`;
  const read = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } };
  const notify = message => {
    const toast = $('#toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(window.dvTimer);
    window.dvTimer = setTimeout(() => toast.classList.remove('visible'), 3000);
  };
  const write = (key, value) => {
    try { localStorage.setItem(key, JSON.stringify(value)); return true; }
    catch { notify('Browser storage is unavailable. Changes last for this visit.'); return false; }
  };
  let saved = read('dv-saved', []);
  if (!Array.isArray(saved)) saved = [];
  saved = [...new Set(saved.filter(id => typeof id === 'string'))];
  const params = new URLSearchParams(location.search);
  const allowed = $$('[data-filter]').map(button => button.dataset.filter);
  let category = params.has('saved') ? 'saved' : params.get('category') || 'All stories';
  if (!allowed.includes(category)) category = 'All stories';

  const syncTheme = () => {
    const dark = document.body.classList.contains('dark');
    const button = $('#theme');
    if (!button) return;
    button.innerHTML = icon(dark ? 'sun' : 'moon');
    button.setAttribute('aria-label', dark ? 'Use light theme' : 'Use dark theme');
    button.setAttribute('aria-pressed', String(dark));
  };
  const preference = read('dv-theme', null);
  document.body.classList.toggle('dark', preference === 'dark' || (!preference && matchMedia('(prefers-color-scheme: dark)').matches));
  syncTheme();
  $('#theme')?.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    write('dv-theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    syncTheme();
  });

  const render = () => {
    $$('.saved-count').forEach(element => { element.textContent = saved.length; });
    $$('[data-save]').forEach(button => {
      const active = saved.includes(button.dataset.save);
      button.setAttribute('aria-pressed', String(active));
      button.innerHTML = icon(active ? 'check' : 'bookmark') + (button.classList.contains('inline') ? (active ? ' Saved' : ' Save') : '');
    });
    if (!$('#search')) return;
    const query = $('#search').value.trim().toLocaleLowerCase('en');
    let count = 0;
    $$('.story').forEach(card => {
      const matchCategory = category === 'All stories' || (category === 'saved' ? saved.includes(card.dataset.slug) : card.dataset.category === category);
      card.hidden = !(matchCategory && card.dataset.search.includes(query));
      if (!card.hidden) count++;
    });
    $$('[data-filter]').forEach(button => {
      const active = button.dataset.filter === category;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    $('#empty').hidden = count !== 0;
    $('#results').textContent = `${count} ${count === 1 ? 'story' : 'stories'} found`;
  };
  $$('[data-save]').forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.save;
    const active = saved.includes(id);
    saved = active ? saved.filter(item => item !== id) : [...saved, id];
    const persisted = write('dv-saved', saved);
    render();
    if (persisted) notify(active ? 'Removed from your reading list' : 'A good idea, saved for later.');
  }));
  $$('[data-filter]').forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; render(); }));
  $('#search')?.addEventListener('input', render);
  $('#reset')?.addEventListener('click', () => { category = 'All stories'; $('#search').value = ''; render(); });
  const menu = $('.menu-button');
  menu?.addEventListener('click', () => {
    const expanded = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(expanded));
    $('#main-nav').classList.toggle('open', expanded);
  });
  $$('#main-nav a').forEach(link => link.addEventListener('click', () => {
    $('#main-nav').classList.remove('open'); menu?.setAttribute('aria-expanded', 'false');
  }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
      $('#main-nav').classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); menu.focus();
    }
  });
  $$('.share').forEach(button => button.addEventListener('click', async () => {
    try {
      if (navigator.share) await navigator.share({ title: document.title, url: location.href });
      else { await navigator.clipboard.writeText(location.href); notify('Article link copied'); }
    } catch (error) { if (error.name !== 'AbortError') notify('Copy the article address from your browser to share it.'); }
  }));
  $('#clear-data')?.addEventListener('click', () => {
    try {
      localStorage.removeItem('dv-saved'); localStorage.removeItem('dv-theme');
      saved = []; document.body.classList.remove('dark'); syncTheme(); render(); notify('Saved articles and theme cleared');
    } catch { notify('Browser storage is unavailable'); }
  });

  $$('[data-calculator], [data-visibility-calculator]').forEach(calculator => {
    const calculate = () => {
      const inputs = $$('input', calculator);
      const values = inputs.map(input => input.value.trim() === '' ? NaN : Number(input.value));
      const result = $('.calculator-result', calculator);
      const output = $('output', calculator);
      const explanation = $('.calculator-explanation', calculator);
      let invalid = !values.every(Number.isFinite);
      let message = 'Enter a finite number in every field.';
      let answer = '';
      if (!invalid && calculator.hasAttribute('data-visibility-calculator')) {
        const [responses, mentions, recommendations] = values;
        invalid = !values.every(Number.isSafeInteger) || responses <= 0 || recommendations < 0 || mentions < 0 || mentions > responses || recommendations > mentions;
        message = 'Use whole counts: responses > 0, and 0 ≤ recommendations ≤ mentions ≤ responses.';
        if (!invalid) {
          answer = `${Number((mentions / responses * 100).toFixed(2))}% / ${Number((recommendations / responses * 100).toFixed(2))}%`;
          message = `${mentions} of ${responses} mention the brand; ${recommendations} of ${responses} explicitly recommend it.`;
        }
      } else if (!invalid) {
        const [minimum, maximum, observation] = values;
        invalid = maximum <= minimum;
        message = 'Training maximum must be greater than minimum. A constant range has no defined result in this formula.';
        if (!invalid) {
          const transformed = (observation - minimum) / (maximum - minimum);
          invalid = !Number.isFinite(transformed);
          if (invalid) message = 'These values exceed the numerical precision supported by this calculator.';
          else {
            answer = String(Number(transformed.toFixed(6)));
            message = `(${observation} − ${minimum}) ÷ (${maximum} − ${minimum}) = ${answer}${transformed < 0 || transformed > 1 ? '. Outside 0–1 because this observation is outside the training bounds; no clipping is applied.' : ''}`;
          }
        }
      }
      result.classList.toggle('invalid', invalid);
      output.textContent = invalid ? 'Check the inputs' : answer;
      explanation.textContent = message;
    };
    calculator.addEventListener('input', calculate); calculate();
  });

  let ticking = false;
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const range = document.documentElement.scrollHeight - innerHeight;
      $('#progress').style.width = `${range > 0 ? Math.min(100, Math.max(0, scrollY / range * 100)) : 0}%`;
      ticking = false;
    });
  }, { passive: true });
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const elements = $$('.story, .manifesto, .topic-link');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
    }, { rootMargin: '0px 0px 80px 0px', threshold: 0 });
    elements.forEach(element => { element.classList.add('reveal'); observer.observe(element); });
    document.body.classList.add('motion-ready');
  }
  render();
})();
