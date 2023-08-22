const textColorNodes = document.querySelectorAll("[data-text-color]");

function textToColor(text) {
  let hash = 0;
  for (let i = 0; i < text.length; i++) {
    hash = text.charCodeAt(i) + ((hash << 5) - hash);
  }
  let color = "#";
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xff;
    color += ("00" + value.toString(16)).substr(-2);
  }
  return color;
}

textColorNodes.forEach((node) => {
  const text = node.dataset.textColor;
  node.style.color = textToColor(text);
});
