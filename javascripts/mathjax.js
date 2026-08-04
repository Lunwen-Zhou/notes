window.MathJax = {
  loader: {
    load: ["[tex]/boldsymbol", "[tex]/textmacros"]
  },
  tex: {
    packages: { "[+]": ["boldsymbol", "textmacros"] },
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

const prepareTocMath = () => {
  const links = document.querySelectorAll(
    ".md-nav--secondary .md-nav__link"
  );

  links.forEach((link) => {
    const walker = document.createTreeWalker(link, NodeFilter.SHOW_TEXT);
    const textNodes = [];

    while (walker.nextNode()) {
      if (!walker.currentNode.parentElement.closest(".arithmatex")) {
        textNodes.push(walker.currentNode);
      }
    }

    textNodes.forEach((textNode) => {
      const parts = textNode.nodeValue.split(/(\\\(.+?\\\))/g);

      if (parts.length === 1) return;

      const fragment = document.createDocumentFragment();
      parts.forEach((part) => {
        if (/^\\\(.+\\\)$/.test(part)) {
          const math = document.createElement("span");
          math.className = "arithmatex";
          math.textContent = part;
          fragment.appendChild(math);
        } else {
          fragment.appendChild(document.createTextNode(part));
        }
      });
      textNode.replaceWith(fragment);
    });
  });
};

document$.subscribe(() => {
  prepareTocMath();
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});
