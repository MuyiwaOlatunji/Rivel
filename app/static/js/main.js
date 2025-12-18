// app/static/js/main.js — Mobile menu + cart count update
document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu toggle
  const mobileBtn = document.querySelector(".mobile-toggle");
  const mobileMenu = document.getElementById("mobile-menu");

  if (mobileBtn && mobileMenu) {
    mobileBtn.addEventListener("click", function () {
      mobileMenu.classList.toggle("hidden");
    });

    // Close when clicking link
    mobileMenu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => mobileMenu.classList.add("hidden"));
    });
  }

  // Update cart badge from session (called by cart.js)
  window.updateCartBadge = function (count) {
    const badge = document.querySelector(".cart-badge");
    if (badge) {
      badge.textContent = count;
      badge.style.display = count > 0 ? "flex" : "none";
    }
  };

  // Initial badge update
  const initialCount = parseInt(document.querySelector(".cart-badge")?.textContent || "0");
  window.updateCartBadge(initialCount);
});