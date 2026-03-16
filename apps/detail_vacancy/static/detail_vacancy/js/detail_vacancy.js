document.addEventListener("DOMContentLoaded", () => {

  // ── Sticky footer on scroll ──────────────────────────────
  const vacancyCard = document.getElementById("vacancy-card-detail");
  const footer      = document.getElementById("vacancy-footer");

  if (vacancyCard && footer) {
    const observer = new IntersectionObserver(
      ([entry]) => footer.classList.toggle("d-none", entry.isIntersecting),
      { threshold: 0.1 }
    );
    observer.observe(vacancyCard);
  }

  // ── More-options dropdown ────────────────────────────────
  const moreBtn  = document.getElementById("more-options-btn");
  const moreMenu = document.getElementById("more-options-menu");

  if (moreBtn && moreMenu) {
    moreBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      moreMenu.classList.toggle("d-none");
    });
    document.addEventListener("click", () => moreMenu.classList.add("d-none"));
  }

  // ── Hide vacancy action ──────────────────────────────────
  document.getElementById("hide-this-vacancy")?.addEventListener("click", () => {
    document.getElementById("vacancy-card-detail")
      ?.closest(".vacancy-card")
      ?.remove();
  });

});