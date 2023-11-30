const searchInput = document.getElementById('search-input');

searchInput.addEventListener(
    "input", () => {
        key = searchInput.value.trim();
        run(1, key);
    }
)
