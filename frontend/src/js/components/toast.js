export function notify(message, { timeoutMs = 4500, tone = 'info' } = {}) {
  const region = document.querySelector('[data-toast-region]');

  if (!region) {
    return;
  }

  const toast = document.createElement('div');
  toast.className = `toast toast--${tone}`;
  toast.setAttribute('role', tone === 'error' ? 'alert' : 'status');

  const copy = document.createElement('span');
  copy.className = 'toast__message';
  copy.textContent = message;

  const dismiss = document.createElement('button');
  dismiss.className = 'toast__dismiss';
  dismiss.type = 'button';
  dismiss.setAttribute('aria-label', 'Dismiss notification');
  dismiss.textContent = 'Dismiss';

  const removeToast = () => toast.remove();
  dismiss.addEventListener('click', removeToast);
  toast.append(copy, dismiss);
  region.append(toast);

  window.setTimeout(removeToast, timeoutMs);
}
