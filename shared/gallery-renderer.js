import { observeFadeIns } from './scroll-animations.js';

const PDF_ICON_SVG = `<svg class="pdf-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M7 21h10a2 2 0 002-2V9l-6-6H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
  <path d="M13 3v6h6"/>
</svg>`;

export function renderGifs(containerId, gifs, basePath = './') {
  const grid = document.getElementById(containerId);
  if (!grid || !gifs.length) return;
  grid.innerHTML = gifs.map(g => `
    <a href="${basePath}gif/${g.id}-${g.file}.gif" class="gif-card fade-in" target="_blank">
      <img src="${basePath}gif/${g.id}-${g.file}.gif" alt="${g.name}" loading="lazy">
      <span class="gif-badge">${g.id} / ${gifs.length}</span>
      <div class="overlay">
        <h3>${g.name}</h3>
        <p>${g.desc} &middot; ${g.palette}</p>
      </div>
    </a>
  `).join('');
}

export function renderPdfs(containerId, pdfs, basePath = './', filter = 'all') {
  const grid = document.getElementById(containerId);
  if (!grid || !pdfs.length) return;
  const filtered = filter === 'all' ? pdfs : pdfs.filter(p => p.series === filter);
  grid.innerHTML = filtered.map(p => `
    <a href="${basePath}${p.n}-${p.file}.pdf" class="pdf-card fade-in" target="_blank">
      ${PDF_ICON_SVG}
      <div class="pdf-number">${p.n}</div>
      <div class="pdf-name">${p.name}</div>
      <div class="pdf-concept">${p.concept}</div>
      <div class="pdf-palette">
        ${p.palette.map(c => `<span class="dot" style="background:${c}"></span>`).join('')}
      </div>
    </a>
  `).join('');
  observeFadeIns();
}

export function renderStandalone(containerId, standalone, basePath = './') {
  const grid = document.getElementById(containerId);
  if (!grid || !standalone.length) return;
  grid.innerHTML = standalone.map(s => {
    const isImage = s.format === 'png' || s.format === 'gif' || s.format === 'svg';
    const preview = isImage
      ? `<img src="${basePath}${s.file}" alt="${s.name}" loading="lazy">`
      : `<div style="color:var(--text2);font-size:0.9rem;">${s.format === 'html' ? 'Interactive' : 'PDF Document'}</div>`;
    return `
      <a href="${basePath}${s.file}" class="standalone-card fade-in" target="_blank">
        <div class="standalone-preview">
          ${preview}
          <span class="format-tag ${s.format}">.${s.format}</span>
        </div>
        <div class="standalone-info">
          <h3>${s.name}</h3>
          <p>${s.desc}</p>
        </div>
      </a>
    `;
  }).join('');
}

export function renderSources(containerId, sources, basePath = './') {
  const grid = document.getElementById(containerId);
  if (!grid || !sources.length) return;
  grid.innerHTML = sources.map(s => `
    <a href="${basePath}${s.file}" class="source-card fade-in" target="_blank">
      <h3>${s.file}</h3>
      <p><strong>${s.name}</strong></p>
      <p style="margin-top:0.4rem">${s.desc}</p>
    </a>
  `).join('');
}

export function initPdfFilters(filterContainerId, pdfContainerId, pdfs, basePath = './') {
  const filterBar = document.getElementById(filterContainerId);
  if (!filterBar) return;
  filterBar.addEventListener('click', e => {
    if (!e.target.classList.contains('filter-btn')) return;
    filterBar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    renderPdfs(pdfContainerId, pdfs, basePath, e.target.dataset.filter);
  });
}
