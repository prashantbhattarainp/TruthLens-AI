const icons = {
  activity: '<path d="M4 12h3l2-7 3 14 2-7h6" />',
  arrowRight: '<path d="M5 12h14" /><path d="m13 6 6 6-6 6" />',
  book: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5z" /><path d="M4 5.5v16" />',
  check: '<path d="m5 12 4 4L19 6" />',
  layers: '<path d="m12 3 9 5-9 5-9-5 9-5Z" /><path d="m3 12 9 5 9-5" /><path d="m3 16 9 5 9-5" />',
  menu: '<path d="M4 7h16M4 12h16M4 17h16" />',
  message: '<path d="M20 15a4 4 0 0 1-4 4H8l-4 3v-7a4 4 0 0 1-2-3.5V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z" />',
  shield: '<path d="M12 3 4.5 6v5.5c0 4.5 3.1 7.7 7.5 9.5 4.4-1.8 7.5-5 7.5-9.5V6z" /><path d="m8.5 12 2.3 2.3 4.8-5" />',
  spark: '<path d="m12 3 1.4 5.6L19 10l-5.6 1.4L12 17l-1.4-5.6L5 10l5.6-1.4z" /><path d="m19 17 .6 2.4L22 20l-2.4.6L19 23l-.6-2.4L16 20l2.4-.6z" />',
};

export function icon(name, { label = null } = {}) {
  const paths = icons[name] ?? icons.spark;
  const accessibleLabel = label ? `<title>${label}</title>` : '';
  const hidden = label ? '' : ' aria-hidden="true"';

  return `<svg class="icon" viewBox="0 0 24 24" role="img"${hidden}>${accessibleLabel}${paths}</svg>`;
}
