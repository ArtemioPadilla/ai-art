import { renderGifs, renderPdfs, renderStandalone, renderSources, initPdfFilters } from './gallery-renderer.js';
import { observeFadeIns } from './scroll-animations.js';

export function renderCollectionPage({ meta, gifs = [], pdfs = [], standalone = [], sources = [], basePath = './' }) {
  const hero = document.getElementById('collection-hero');
  const content = document.getElementById('collection-content');
  if (!hero || !content) return;

  // Build stats from available data
  const stats = [];
  if (pdfs.length) stats.push({ value: pdfs.length, label: 'PDF Posters', color: 'purple' });
  if (gifs.length) stats.push({ value: gifs.length, label: 'Animated GIFs', color: 'cyan' });
  if (standalone.length) stats.push({ value: standalone.length, label: 'Standalone Pieces', color: 'rose' });
  if (sources.length) stats.push({ value: sources.length, label: 'Generator Scripts', color: 'gold' });

  // Render hero
  hero.innerHTML = `
    <div class="hero-content">
      <h1>${meta.name}</h1>
      <p class="subtitle">${meta.tagline}</p>
      <div class="stats">
        ${stats.map(s => `
          <div class="stat">
            <div class="stat-number ${s.color}">${s.value}</div>
            <div class="stat-label">${s.label}</div>
          </div>
        `).join('')}
      </div>
      <nav class="nav-pills">
        <a href="../../" class="nav-pill">All Collections</a>
        ${gifs.length ? '<a href="#gifs" class="nav-pill">Animated GIFs</a>' : ''}
        ${pdfs.length ? '<a href="#posters" class="nav-pill">PDF Posters</a>' : ''}
        ${standalone.length ? '<a href="#standalone" class="nav-pill">Standalone</a>' : ''}
        ${sources.length ? '<a href="#source" class="nav-pill">Source Code</a>' : ''}
      </nav>
    </div>
  `;

  // Build sections
  let sections = '';

  if (gifs.length) {
    sections += `
      <section id="gifs">
        <div class="section-header fade-in">
          <h2>Animated GIFs</h2>
          <div class="divider"></div>
          <p>${gifs.length} perfectly looping animations. Sacred geometry in motion.</p>
        </div>
        <div class="gif-grid" id="gif-grid"></div>
      </section>
    `;
  }

  if (pdfs.length) {
    // Compute series for filter buttons
    const seriesSet = [...new Set(pdfs.map(p => p.series))].sort();
    sections += `
      <section id="posters">
        <div class="section-header fade-in">
          <h2>PDF Posters</h2>
          <div class="divider"></div>
          <p>${pdfs.length} unique A3 vector PDFs exploring geometry, fractals, physics, and mathematical beauty.</p>
        </div>
        <div class="filter-bar" id="pdf-filters">
          <button class="filter-btn active" data-filter="all">All (${pdfs.length})</button>
          ${seriesSet.map(s => `<button class="filter-btn" data-filter="${s}">${s}</button>`).join('')}
        </div>
        <div class="pdf-grid" id="pdf-grid"></div>
      </section>
    `;
  }

  if (standalone.length) {
    sections += `
      <section id="standalone">
        <div class="section-header fade-in">
          <h2>Standalone Pieces</h2>
          <div class="divider"></div>
          <p>Individual artworks in various formats — PNG, GIF, PDF, SVG, and interactive HTML.</p>
        </div>
        <div class="standalone-grid" id="standalone-grid"></div>
      </section>
    `;
  }

  if (sources.length) {
    sections += `
      <section id="source">
        <div class="section-header fade-in">
          <h2>Source Code</h2>
          <div class="divider"></div>
          <p>Every piece is generated from Python scripts. Explore, fork, and create your own.</p>
        </div>
        <div class="source-grid" id="source-grid"></div>
      </section>
    `;
  }

  content.innerHTML = sections;

  // Render content into sections
  if (gifs.length) renderGifs('gif-grid', gifs, basePath);
  if (pdfs.length) {
    renderPdfs('pdf-grid', pdfs, basePath);
    initPdfFilters('pdf-filters', 'pdf-grid', pdfs, basePath);
  }
  if (standalone.length) renderStandalone('standalone-grid', standalone, basePath);
  if (sources.length) renderSources('source-grid', sources, basePath);

  observeFadeIns();
}
