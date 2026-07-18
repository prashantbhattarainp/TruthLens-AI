export function createModal({ content, id, title }) {
  const dialog = document.createElement('dialog');

  dialog.className = 'modal';
  dialog.id = id;
  dialog.setAttribute('aria-labelledby', `${id}-title`);
  dialog.innerHTML = `
    <div class="modal__content">
      <h2 id="${id}-title">${title}</h2>
      <div>${content}</div>
      <div class="modal__actions">
        <button class="button button--primary" type="button" data-modal-close>Close</button>
      </div>
    </div>
  `;
  dialog.querySelector('[data-modal-close]')?.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });

  return dialog;
}
