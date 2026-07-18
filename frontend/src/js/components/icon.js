const icons = {
  activity: '<path d="M4 12h3l2-7 3 14 2-7h6" />',
  arrowRight: '<path d="M5 12h14" /><path d="m13 6 6 6-6 6" />',
  brain: '<path d="M9 4a3 3 0 0 0-5 2.2A3.5 3.5 0 0 0 5 13a3 3 0 0 0 4 4.7A3.5 3.5 0 0 0 12 20V4" /><path d="M15 4a3 3 0 0 1 5 2.2A3.5 3.5 0 0 1 19 13a3 3 0 0 1-4 4.7A3.5 3.5 0 0 1 12 20V4" /><path d="M8 9h4M12 15H9M16 9h-4M12 15h3" />',
  book: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5z" /><path d="M4 5.5v16" />',
  clock: '<circle cx="12" cy="12" r="8.5" /><path d="M12 7v5l3.5 2" />',
  database: '<ellipse cx="12" cy="5" rx="7.5" ry="2.5" /><path d="M4.5 5v7c0 1.4 3.4 2.5 7.5 2.5s7.5-1.1 7.5-2.5V5" /><path d="M4.5 12v7c0 1.4 3.4 2.5 7.5 2.5s7.5-1.1 7.5-2.5v-7" />',
  check: '<path d="m5 12 4 4L19 6" />',
  layers: '<path d="m12 3 9 5-9 5-9-5 9-5Z" /><path d="m3 12 9 5 9-5" /><path d="m3 16 9 5 9-5" />',
  menu: '<path d="M4 7h16M4 12h16M4 17h16" />',
  message: '<path d="M20 15a4 4 0 0 1-4 4H8l-4 3v-7a4 4 0 0 1-2-3.5V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z" />',
  refresh: '<path d="M20 11a8 8 0 1 0 1.5 5" /><path d="M20 4v7h-7" />',
  server: '<rect x="4" y="4" width="16" height="6" rx="1" /><rect x="4" y="14" width="16" height="6" rx="1" /><path d="M8 7h.01M8 17h.01M12 7h5M12 17h5" />',
  shield: '<path d="M12 3 4.5 6v5.5c0 4.5 3.1 7.7 7.5 9.5 4.4-1.8 7.5-5 7.5-9.5V6z" /><path d="m8.5 12 2.3 2.3 4.8-5" />',
  spark: '<path d="m12 3 1.4 5.6L19 10l-5.6 1.4L12 17l-1.4-5.6L5 10l5.6-1.4z" /><path d="m19 17 .6 2.4L22 20l-2.4.6L19 23l-.6-2.4L16 20l2.4-.6z" />',
};

export function icon(name, { label = null } = {}) {
  const paths = icons[name] ?? icons.spark;
  const accessibleLabel = label ? `<title>${label}</title>` : '';
  const hidden = label ? '' : ' aria-hidden="true"';

  return `<svg class="icon" viewBox="0 0 24 24" role="img"${hidden}>${accessibleLabel}${paths}</svg>`;
}
