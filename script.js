const searchInput = document.getElementById("search-input");
const genreFilter = document.getElementById("genre-filter");
const movieGrid = document.getElementById("movie-grid");
const movieCount = document.getElementById("movie-count");
const emptyState = document.getElementById("empty-state");
const chips = document.getElementById("genre-chips");
let selectedGenre = "";

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function movieCard(movie) {
  const title = escapeHTML(movie.title);
  const genres = movie.genres.map(escapeHTML).join(" / ");
  const description = escapeHTML(movie.description);
  const poster = escapeHTML(movie.poster);
  return `
    <article class="movie-card" data-id="${movie.id}">
      <button class="poster-button" data-movie="${movie.id}" aria-label="Find movies similar to ${title}">
        <img class="poster" src="${poster}" alt="${title} poster" loading="lazy"
          onerror="this.onerror=null;this.src='https://placehold.co/400x600/17152a/f4d9a6?text=Movie+Poster';">
        <span class="poster-overlay"><span>✦ Find similar movies</span></span>
      </button>
      <div class="movie-info">
        <div class="movie-title-row"><h3>${title}</h3><span class="rating">★ ${movie.rating}</span></div>
        <div class="movie-meta">${movie.year} <span>•</span> ${genres}</div>
        <p>${description}</p>
        <button class="text-btn recommend-btn" data-movie="${movie.id}">Find similar <span>↗</span></button>
      </div>
    </article>`;
}

async function loadMovies() {
  const params = new URLSearchParams();
  params.set("q", searchInput.value.trim());
  params.set("genre", selectedGenre);
  try {
    const response = await fetch(`/api/movies?${params.toString()}`);
    if (!response.ok) throw new Error("Could not load movies");
    const movies = await response.json();
    movieGrid.innerHTML = movies.map(movieCard).join("");
    movieCount.textContent = movies.length;
    emptyState.hidden = movies.length !== 0;
    movieGrid.hidden = movies.length === 0;
  } catch (error) {
    emptyState.hidden = false;
    movieGrid.hidden = true;
    emptyState.querySelector("h3").textContent = "Could not load movies";
    emptyState.querySelector("p").textContent = "Please refresh the page and try again.";
  }
}

function chooseGenre(genre) {
  selectedGenre = genre;
  genreFilter.value = genre;
  chips.querySelectorAll(".chip").forEach((chip) => {
    chip.classList.toggle("active", chip.dataset.genre === genre);
  });
  loadMovies();
}

searchInput.addEventListener("input", loadMovies);
genreFilter.addEventListener("change", () => chooseGenre(genreFilter.value));
chips.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-genre]");
  if (button) chooseGenre(button.dataset.genre);
});
document.getElementById("reset-search").addEventListener("click", () => {
  searchInput.value = "";
  chooseGenre("");
});

const recommendationSection = document.getElementById("recommendations");
const recommendationGrid = document.getElementById("recommend-grid");

async function showRecommendations(movieId) {
  try {
    const response = await fetch(`/api/recommend/${movieId}`);
    if (!response.ok) throw new Error("Could not get recommendations");
    const matches = await response.json();
    const sourceCard = document.querySelector(`.movie-card[data-id="${movieId}"]`);
    const sourceTitle = sourceCard?.querySelector("h3")?.textContent || "your pick";
    document.getElementById("selected-title").textContent = sourceTitle;
    recommendationGrid.innerHTML = matches.length ? matches.map((movie) => `
      <article class="recommend-card">
        <img src="${escapeHTML(movie.poster)}" alt="${escapeHTML(movie.title)} poster"
          onerror="this.onerror=null;this.src='https://placehold.co/400x600/17152a/f4d9a6?text=Movie+Poster';">
        <div>
          <span class="match">${movie.match}% feature match</span>
          <h3>${escapeHTML(movie.title)}</h3>
          <div class="movie-meta">${movie.year} · ★ ${movie.rating}</div>
          <p>${escapeHTML(movie.description)}</p>
          <div class="movie-meta">${movie.genres.map(escapeHTML).join(" / ")}</div>
        </div>
      </article>`).join("") : "<p>No similar movies found in this demo catalogue.</p>";
    recommendationSection.hidden = false;
    recommendationSection.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    alert("Sorry, recommendations could not be loaded. Please try again.");
  }
}

document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-movie]");
  if (button) showRecommendations(Number(button.dataset.movie));
});
document.getElementById("close-recommendations").addEventListener("click", () => {
  recommendationSection.hidden = true;
});
