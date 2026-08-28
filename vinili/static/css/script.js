const DISCOGS_TOKEN = "sfJSPxBiwqOeMNTYfmTcNSibzLFsEdvlxvSWdhGV"; 

async function caricaSezione(query, elementId, limite = 4) {
    const container = document.getElementById(elementId);
    if (!container) return; 

    const url = `https://api.discogs.com/database/search?q=${query}&type=release&format=vinyl&per_page=${limite}`;

    try {
        const response = await fetch(url, {
            headers: { 
                'Authorization': `Discogs token=${DISCOGS_TOKEN}`,
                'User-Agent': 'RitmoSanchezApp/1.0'
            }
        });
        const data = await response.json();
        
        // Se è la prima chiamata (es. 2026), svuotiamo. 
        // Se vuoi sommare i risultati, togli container.innerHTML = '';
        container.innerHTML = ''; 

        data.results.forEach(disco => {
            const parti = disco.title.split(' - ');
            // Questa è la riga fondamentale per il collegamento a Django
            container.innerHTML += `
                <article class="card">
                    <div>
                        <img src="${disco.cover_image}" alt="${disco.title}">
                        <h3>${parti[1] || "Album"}</h3>
                        <p>${parti[0] || "Artista"}</p>
                    </div> 
                    <a href="/vinile/${disco.id}/" class="btn">Vedi Dettaglio</a>
                </article>
            `;
        });
    } catch (error) {
        console.error("Errore Discogs:", error);
    }
}

// Gestione Password (Login)
function inizializzaTogglePassword() {
    const toggleBtn = document.querySelector('#togglePassword');
    // Django di solito assegna l'id 'id_password' al campo password
    const passwordField = document.querySelector('input[type="password"]');

    if (toggleBtn && passwordField) {
        toggleBtn.addEventListener('click', function (e) {
            // Impedisce al form di essere inviato se il bottone è dentro il tag form
            e.preventDefault(); 
            
            const isPassword = passwordField.getAttribute('type') === 'password';
            
            // Cambia il tipo tra password e text
            passwordField.setAttribute('type', isPassword ? 'text' : 'password');
            
            // Cambia il testo del pulsante
            this.textContent = isPassword ? 'NASCONDI' : 'MOSTRA';
        });
    }
}

// Evento principale al caricamento della pagina
document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. CARICAMENTO INIZIALE (Appena apri la pagina) ---
    // Carica i dischi del 2016 nella prima griglia
    caricaSezione('2016', 'grid-selezione', 8);
    
    // Carica i dischi Trending (es. genere Jazz o Techno) nella seconda griglia
    caricaSezione('Jazz', 'grid-trending', 8);


    // --- 2. GESTIONE RICERCA ---
    const searchForm = document.getElementById('search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = document.getElementById('search-input').value.trim();
            
            if (query) {
                // Modifichiamo il titolo della prima sezione
                const titolo = document.getElementById('titolo-selezione');
                if (titolo) titolo.innerText = `Risultati per: ${query}`;
                
                // Carichiamo i risultati della ricerca solo nella prima griglia
                caricaSezione(query, 'grid-selezione', 16);

                // NASCONDIAMO la sezione Trending per lasciare spazio alla ricerca
                const sezioneTrending = document.getElementById('sezione-trending');
                if (sezioneTrending) {
                    sezioneTrending.style.display = 'none';
                }
            }
        });
    }


async function inizializzaDettaglio() {
    const container = document.getElementById('dettaglio-container');
    if (!container) return; // Se non siamo nella pagina dettaglio, esci

    const idDisco = container.getAttribute('data-id');
    const url = `https://api.discogs.com/releases/${idDisco}`;

    try {
        const response = await fetch(url, {
            headers: { 'Authorization': `Discogs token=${DISCOGS_TOKEN}` }
        });
        const data = await response.json();

        container.innerHTML = `
            <div style="display: flex; gap: 40px; padding: 40px 0; align-items: start;">
                <div style="flex: 1;">
                    <img src="${data.images ? data.images[0].uri : 'https://via.placeholder.com/600'}" 
                         alt="${data.title}" 
                         style="width: 100%; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                </div>
                <div style="flex: 1;">
                    <h1 style="font-size: 2.5rem; margin-bottom: 10px;">${data.title}</h1>
                    <p style="font-size: 1.5rem; color: var(--text-secondary); margin-bottom: 20px;">
                        ${data.artists_sort}
                    </p>
                    <div style="margin-top: 20px; border-top: 1px solid var(--border-color); padding-top: 20px;">
                        <p style="margin-bottom: 10px;"><strong>Genere:</strong> ${data.genres ? data.genres.join(', ') : 'N/D'}</p>
                        <p style="margin-bottom: 10px;"><strong>Anno:</strong> ${data.year || 'N/D'}</p>
                        <p style="margin-bottom: 10px;"><strong>Etichetta:</strong> ${data.labels ? data.labels[0].name : 'N/D'}</p>
                        <p style="font-size: 1.8rem; color: var(--accent-color); margin-top: 20px; font-weight: bold;">€ 29.90</p>
                    </div>
                    <button class="btn" style="margin-top: 30px; width: auto; padding: 15px 40px;">AGGIUNGI AL CARRELLO</button>
                </div>
            </div>`;
    } catch (error) {
        container.innerHTML = "<h1>Errore nel caricamento del disco.</h1>";
    }
}

    // 3. Attiva toggle password
    inizializzaDettaglio();
    inizializzaTogglePassword(); 
});