import { renderFooter } from './components/footer.js';
import { renderNavigation } from './components/navigation.js';
import { initializeDetectionInterface } from './modules/detection-interface.js';

const activePage = document.body.dataset.page;

renderNavigation(activePage);
renderFooter();
initializeDetectionInterface();
