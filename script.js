function handleSearch() {
  const query = document.getElementById('searchQuery').value.trim();
  if (!query) return false;
  window.location.href = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
  return false;
}

function openSiteDialog() {
  document.getElementById('dialogError').textContent = '';
  document.getElementById('siteForm').reset();
  document.getElementById('siteDialog').showModal();
  document.getElementById('siteName').focus();
}

function closeSiteDialog() {
  document.getElementById('siteDialog').close();
}

async function saveSite(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const error = document.getElementById('dialogError');
  const data = Object.fromEntries(new FormData(form));

  try {
    const response = await fetch('/api/sites', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'No se pudo guardar el sitio.');

    window.dashboardSites = result.sites;
    renderSites(window.dashboardSites);
    closeSiteDialog();
  } catch (error) {
    document.getElementById('dialogError').textContent = error.message;
  }
}

function createFallbackLogo(name) {
  const initials = name.trim().slice(0, 2).toUpperCase();
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80"><rect width="80" height="80" rx="16" fill="#4a90e2"/><text x="40" y="48" fill="white" font-family="Arial,sans-serif" font-size="26" font-weight="bold" text-anchor="middle">${initials}</text></svg>`;
  return `data:image/svg+xml,${encodeURIComponent(svg)}`;
}

function renderSites(sites) {
  const grid = document.getElementById('linksGrid');
  grid.innerHTML = '';

  sites.forEach((site, index) => {
    const card = document.createElement('a');
    card.className = 'card';
    card.href = site.url;

    const image = document.createElement('img');
    image.src = site.photo || createFallbackLogo(site.name);
    image.alt = site.name;

    const label = document.createElement('span');
    label.textContent = site.name;

    card.append(image, label);

    if (document.body.classList.contains('editing-sites')) {
      const deleteButton = document.createElement('button');
      deleteButton.className = 'delete-site-button';
      deleteButton.type = 'button';
      deleteButton.title = `Eliminar ${site.name}`;
      deleteButton.setAttribute('aria-label', `Eliminar ${site.name}`);
      deleteButton.textContent = '×';
      deleteButton.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        deleteSite(index);
      });
      card.appendChild(deleteButton);
    }

    grid.appendChild(card);
  });
}

async function deleteSite(index) {
  if (!window.confirm(`¿Eliminar "${window.dashboardSites[index].name}"?`)) return;

  try {
    const response = await fetch(`/api/sites/${index}`, { method: 'DELETE' });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'No se pudo eliminar el sitio.');
    window.dashboardSites = result.sites;
    renderSites(window.dashboardSites);
  } catch (error) {
    window.alert(error.message);
  }
}

function toggleEditMode() {
  document.body.classList.toggle('editing-sites');
  const editing = document.body.classList.contains('editing-sites');
  document.getElementById('addSiteButton').hidden = !editing;
  document.getElementById('editSitesButton').setAttribute('aria-label', editing ? 'Cerrar edición' : 'Editar sitios');
  document.getElementById('editSitesButton').title = editing ? 'Cerrar edición' : 'Editar sitios';
  renderSites(window.dashboardSites);
}

async function loadSites() {
  const grid = document.getElementById('linksGrid');

  try {
    const response = await fetch('sites.json');
    const sites = await response.json();
    window.dashboardSites = sites;
    renderSites(sites);
  } catch (error) {
    console.error('Error cargando el JSON:', error);
    grid.innerHTML = '<p>Error al cargar sitios. Asegúrate de usar un servidor local.</p>';
  }
}

document.getElementById('addSiteButton').hidden = true;
document.getElementById('editSitesButton').addEventListener('click', toggleEditMode);
document.getElementById('addSiteButton').addEventListener('click', openSiteDialog);
document.getElementById('cancelSiteButton').addEventListener('click', closeSiteDialog);
document.getElementById('siteForm').addEventListener('submit', saveSite);
window.addEventListener('load', loadSites);