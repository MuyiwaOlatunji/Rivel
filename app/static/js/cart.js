// app/static/js/cart.js — FINAL: Toast + Cart count + Clear cart
document.addEventListener("DOMContentLoaded", function () {
  // Toast container
  const toastContainer = document.createElement("div");
  toastContainer.className = "fixed top-24 right-6 z-50 space-y-4";
  document.body.appendChild(toastContainer);

  function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `max-w-sm bg-white border-l-4 ${type === 'success' ? 'border-green-500' : 'border-red-500'} shadow-2xl rounded-lg p-4 flex items-center gap-4 animate-slide-in-right`;
    toast.innerHTML = `
      <i class="fas fa-${type === 'success' ? 'check-circle text-green-600' : 'exclamation-circle text-red-600'} text-2xl"></i>
      <p class="font-medium text-gray-800">${message}</p>
      <button class="ml-auto text-gray-400 hover:text-gray-600">
        <i class="fas fa-times"></i>
      </button>
    `;
    toast.querySelector("button").addEventListener("click", () => toast.remove());
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  }

  // Update cart badge
  function updateCartBadge(count) {
    const badge = document.querySelector(".cart-badge");
    if (badge) {
      badge.textContent = count;
      badge.style.display = count > 0 ? "flex" : "none";
    }
  }

  // Load initial cart count
  fetch('/cart-count')
    .then(res => res.json())
    .then(data => updateCartBadge(data.count))
    .catch(() => updateCartBadge(0));

  // Add to cart
  document.querySelectorAll(".add-to-cart").forEach(button => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const productId = this.dataset.id;

      fetch(`/add-to-cart/${productId}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            showToast(data.message, "success");
            updateCartBadge(data.total_items);
          } else {
            showToast(data.message, "error");
          }
        });
    });
  });

  // Clear cart button
  const clearBtn = document.getElementById("clear-cart");
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      fetch('/clear-cart', { method: "POST" })
        .then(() => {
          location.reload();
        });
    });
  }
});