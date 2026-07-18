export function createModal({ content, id, title }) {
  const dialog = document.createElement('dialog');
  const contentContainer = document.createElement('div');
  const heading = document.createElement('h2');
  const modalContent = document.createElement('div');
  const actions = document.createElement('div');
  const closeButton = document.createElement('button');

  dialog.className = 'modal';
  dialog.id = id;
  dialog.setAttribute('aria-labelledby', `${id}-title`);
  contentContainer.className = 'modal__content';
  heading.id = `${id}-title`;
  heading.textContent = title;
  modalContent.textContent = content;
  actions.className = 'modal__actions';
  closeButton.className = 'button button--primary';
  closeButton.type = 'button';
  closeButton.dataset.modalClose = '';
  closeButton.textContent = 'Close';
  actions.append(closeButton);
  contentContainer.append(heading, modalContent, actions);
  dialog.append(contentContainer);

  closeButton.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });

  return dialog;
}
