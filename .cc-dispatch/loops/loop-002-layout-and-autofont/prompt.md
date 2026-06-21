Read goal.md first. Then:
Phase A: add colorSchema: light + background: '#ffffff' to slides.md headmatter.
Phase B: remove .codeblock-canvas and its CSS; replace with .codeblock-fill (width/height 100%, flex center).
Phase C: remove fixed fontSize prop; add ResizeObserver-based auto font size (calcFontSize using CHAR_WIDTH_RATIO=0.603 and LINE_HEIGHT=1.45); change overflow to hidden on .codeblock-code and pre.shiki.
Phase D: pad shorter snippet in slide 12 with trailing newlines to equalize line counts.
Phase E: wrap each story slide's CodeBlock in a flex column layout so the component has a sized container to fill.
Restart dev server. Screenshot slides 1, 7, 12 in headless Chromium. Write report.md, notify, stop.
