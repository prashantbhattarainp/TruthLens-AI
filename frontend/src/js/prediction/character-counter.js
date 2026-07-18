function formatCharacterCount(currentCount, maximumCount) {
  return `${currentCount.toLocaleString()} / ${maximumCount.toLocaleString()} characters`;
}

function updateCounter(inputElement, counterElement) {
  counterElement.textContent = formatCharacterCount(
    inputElement.value.length,
    inputElement.maxLength,
  );
}

export function initializeCharacterCounters(counterPairs) {
  counterPairs.forEach(({ counterElement, inputElement }) => {
    inputElement.addEventListener('input', () => updateCounter(inputElement, counterElement));
    updateCounter(inputElement, counterElement);
  });

  return () => {
    counterPairs.forEach(({ counterElement, inputElement }) => {
      updateCounter(inputElement, counterElement);
    });
  };
}
