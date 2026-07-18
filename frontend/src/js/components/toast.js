export function notify(message, { timeoutMs = 4500 } = {}) {
  const region = document.querySelector('[data-toast-region]');

  if (!region) {
    return;
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  region.append(toast);

  window.setTimeout(() => toast.remove(), timeoutMs);
}
