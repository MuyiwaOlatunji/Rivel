// app/static/js/main.js — Mobile menu + Cart badge + Email popup
document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu (if added later)
  const mobileBtn = document.querySelector(".mobile-toggle");
  const mobileMenu = document.getElementById("mobile-menu");
  if (mobileBtn && mobileMenu) {
    mobileBtn.addEventListener("click", () => mobileMenu.classList.toggle("hidden"));
    mobileMenu.querySelectorAll("a").forEach(link => link.addEventListener("click", () => mobileMenu.classList.add("hidden")));
  }

  // Cart badge update
  window.updateCartBadge = function (count) {
    const badge = document.querySelector(".cart-badge");
    if (badge) {
      badge.textContent = count;
      badge.style.display = count > 0 ? "flex" : "none";
    }
  };
  fetch('/cart-count').then(res => res.json()).then(data => updateCartBadge(data.count));

  // Email registration popup on first visit
  if (!localStorage.getItem('rivel_welcome_shown')) {
    const popup = document.createElement('div');
    popup.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    popup.innerHTML = `
      <div class="bg-white p-8 rounded-2xl max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-4">Welcome to RIVEL!</h2>
        <p class="mb-6">Sign in with Google for personalized recommendations and fast checkout.</p>
        <a href="/login/google" class="w-full bg-primary text-white py-3 rounded font-bold block text-center mb-4">Sign in with Google</a>
        <button onclick="this.closest('.fixed').remove(); localStorage.setItem('rivel_welcome_shown', 'true')" class="text-gray-500">Skip for now</button>
      </div>
    `;
    document.body.appendChild(popup);
    localStorage.setItem('rivel_welcome_shown', 'true');
  }
});