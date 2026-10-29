function handleSearch() {
  const query = document.getElementById('searchQuery').value.trim();
  if (!query) return false;
  window.location.href = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
  return false;
}

async function loadSites() {
  const grid = document.getElementById('linksGrid');
  
  try {
    const response = await fetch('sites.json');
    const sites = await response.json();
    
    grid.innerHTML = '';

    sites.forEach(site => {
      const card = document.createElement('a');
      card.className = 'card';
      card.href = site.url;
      
      const photoUrl = site.photo || 'https://via.placeholder.com/80?text=Web';
      
      card.innerHTML = `
        <img src="${photoUrl}" alt="${site.name}">
        <span>${site.name}</span>
      `;
      
      grid.appendChild(card);
    });
  } catch (error) {
    console.error("Error cargando el JSON:", error);
    grid.innerHTML = '<p>Error al cargar sitios. Asegúrate de usar un servidor local.</p>';
  }
}

window.onload = loadSites;