const form = document.querySelector("#chatForm");
const input = document.querySelector("#promptInput");
const sendButton = document.querySelector("#sendBtn");
const conversation = document.querySelector("#conversation");
const emptyState = document.querySelector("#emptyState");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatInline(value) {
  let html = escapeHtml(value);
  const codeTokens = [];

  html = html.replace(/`([^`]+)`/g, (_, code) => {
    const token = `@@CODE_${codeTokens.length}@@`;
    codeTokens.push(`<code class="inline-code">${code}</code>`);
    return token;
  });

  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, (_, label, href) => {
    return `<a class="response-link" href="${href}" target="_blank" rel="noreferrer">${label}</a>`;
  });

  return html.replace(/@@CODE_(\d+)@@/g, (_, index) => codeTokens[Number(index)]);
}

function isTableSeparator(line) {
  return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
}

function splitTableRow(line) {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function renderTable(headerLine, rowLines) {
  const headers = splitTableRow(headerLine);
  const rows = rowLines.map(splitTableRow);
  return `
    <div class="response-table-wrap">
      <table class="response-table">
        <thead><tr>${headers.map((cell) => `<th>${formatInline(cell)}</th>`).join("")}</tr></thead>
        <tbody>${rows
          .map((row) => `<tr>${headers.map((_, index) => `<td>${formatInline(row[index] || "")}</td>`).join("")}</tr>`)
          .join("")}</tbody>
      </table>
    </div>`;
}

function renderResponse(source) {
  const lines = String(source || "").replaceAll("\r\n", "\n").split("\n");
  const blocks = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];

    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (line.trim().startsWith("```")) {
      const language = line.trim().slice(3).trim() || "text";
      const codeLines = [];
      index += 1;
      while (index < lines.length && !lines[index].trim().startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length) index += 1;
      blocks.push(`
        <div class="response-code">
          <div class="code-toolbar">
            <span class="code-language">${escapeHtml(language)}</span>
            <button class="copy-code" type="button" aria-label="Copy code">
              <span>Copy</span>
            </button>
          </div>
          <pre>${escapeHtml(codeLines.join("\n"))}</pre>
        </div>`);
      continue;
    }

    if (/^#\s+/.test(line)) {
      blocks.push(`<h1 class="response-title">${formatInline(line.replace(/^#\s+/, ""))}</h1>`);
      index += 1;
      continue;
    }

    if (/^##\s+/.test(line)) {
      blocks.push(`<h2 class="response-section-title">${formatInline(line.replace(/^##\s+/, ""))}</h2>`);
      index += 1;
      continue;
    }

    if (/^###\s+/.test(line)) {
      blocks.push(`<h3 class="response-subtitle">${formatInline(line.replace(/^###\s+/, ""))}</h3>`);
      index += 1;
      continue;
    }

    if (line.includes("|") && index + 1 < lines.length && isTableSeparator(lines[index + 1])) {
      const rowLines = [];
      index += 2;
      while (index < lines.length && lines[index].includes("|") && lines[index].trim()) {
        rowLines.push(lines[index]);
        index += 1;
      }
      blocks.push(renderTable(line, rowLines));
      continue;
    }

    if (/^\s*[-*]\s+/.test(line)) {
      const items = [];
      while (index < lines.length && /^\s*[-*]\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*[-*]\s+/, ""));
        index += 1;
      }
      blocks.push(`<ul class="response-list">${items.map((item) => `<li>${formatInline(item)}</li>`).join("")}</ul>`);
      continue;
    }

    if (/^\s*\d+[.)]\s+/.test(line)) {
      const items = [];
      while (index < lines.length && /^\s*\d+[.)]\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*\d+[.)]\s+/, ""));
        index += 1;
      }
      blocks.push(`<ol class="response-list">${items.map((item) => `<li>${formatInline(item)}</li>`).join("")}</ol>`);
      continue;
    }

    if (/^>\s?/.test(line)) {
      const quoteLines = [];
      while (index < lines.length && /^>\s?/.test(lines[index])) {
        quoteLines.push(lines[index].replace(/^>\s?/, ""));
        index += 1;
      }
      blocks.push(`<blockquote class="response-callout">${quoteLines.map(formatInline).join("<br />")}</blockquote>`);
      continue;
    }

    const paragraphLines = [];
    while (
      index < lines.length &&
      lines[index].trim() &&
      !/^#\s+|^##\s+|^###\s+|^\s*[-*]\s+|^\s*\d+[.)]\s+|^>\s?/.test(lines[index])
    ) {
      if (lines[index].includes("|") && index + 1 < lines.length && isTableSeparator(lines[index + 1])) break;
      if (lines[index].trim().startsWith("```")) break;
      paragraphLines.push(lines[index].trim());
      index += 1;
    }
    blocks.push(`<p class="response-copy">${paragraphLines.map(formatInline).join(" ")}</p>`);
  }

  return blocks.join("");
}

function appendUserMessage(message) {
  const bubble = document.createElement("p");
  bubble.className = "user-message";
  bubble.textContent = message;
  conversation.append(bubble);
}

function appendThinkingMessage() {
  const row = document.createElement("div");
  row.className = "thinking-row";
  row.textContent = "Thinking";
  conversation.append(row);
  return row;
}

function appendError(message, retry) {
  const card = document.createElement("div");
  card.className = "error-card";
  const copy = document.createElement("span");
  copy.textContent = message;
  card.append(copy);

  const retryButton = document.createElement("button");
  retryButton.type = "button";
  retryButton.className = "retry-button";
  retryButton.textContent = "Retry";
  retryButton.addEventListener("click", () => {
    card.remove();
    retry();
  });
  card.append(retryButton);
  conversation.append(card);
  return card;
}

// Route labels shown in the meta line -- matches what /chat actually
// returns (route, sources, latency_seconds), not a fake model name.
const ROUTE_LABELS = {
  general: "GENERAL",
  document: "DOCUMENT",
  tool: "TOOL",
};

function appendAssistantMessage(payload, clientElapsedSeconds) {
  const article = document.createElement("article");
  article.className = "assistant-message";

  const route = ROUTE_LABELS[payload.route] || (payload.route || "UNKNOWN").toUpperCase();
  const latency = typeof payload.latency_seconds === "number" ? payload.latency_seconds : clientElapsedSeconds;

  const meta = document.createElement("div");
  meta.className = "response-meta";
  meta.innerHTML = `
    <span class="model-name">ThunAI · ${escapeHtml(route)}</span>
    <span class="separator">·</span>
    <span>${latency.toFixed(1)}s</span>`;

  const content = document.createElement("div");
  content.className = "response-content";
  content.innerHTML = renderResponse(payload.response || "No response was returned.");

  article.append(meta, content);

  // Show cited sources when the DOCUMENT route retrieved anything --
  // this is the "source-backed, auditable answers" part of the pitch,
  // made visible instead of silently returned and dropped.
  if (Array.isArray(payload.sources) && payload.sources.length) {
    const sourcesList = document.createElement("ul");
    sourcesList.className = "response-list";
    sourcesList.innerHTML = payload.sources
      .map((entry) => `<li>Source: ${escapeHtml(entry.document || "unknown")}</li>`)
      .join("");
    article.append(sourcesList);
  }

  conversation.append(article);
  attachCopyButtons(article);
  article.scrollIntoView({ behavior: "smooth", block: "start" });
}

function attachCopyButtons(container) {
  container.querySelectorAll(".copy-code").forEach((button) => {
    button.addEventListener("click", async () => {
      const code = button.closest(".response-code")?.querySelector("pre")?.textContent || "";
      try {
        await navigator.clipboard.writeText(code);
        button.classList.add("is-copied");
        const label = button.querySelector("span:last-child");
        if (label) label.textContent = "Copied";
        window.setTimeout(() => {
          button.classList.remove("is-copied");
          if (label) label.textContent = "Copy";
        }, 1800);
      } catch {
        const label = button.querySelector("span:last-child");
        if (label) label.textContent = "Select code";
      }
    });
  });
}

function resizeInput() {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 160)}px`;
}

async function submitMessage(message, { appendUser = true } = {}) {
  if (!message.trim()) return;
  if (appendUser) appendUserMessage(message);
  emptyState?.classList.add("is-hidden");
  const thinking = appendThinkingMessage();
  const startedAt = performance.now();
  form.setAttribute("aria-busy", "true");
  input.disabled = true;
  sendButton.disabled = true;

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) throw new Error(`Request failed (${response.status})`);
    const payload = await response.json();
    thinking.remove();
    appendAssistantMessage(payload, (performance.now() - startedAt) / 1000);
  } catch (error) {
    thinking.remove();
    appendError("The request could not be completed. Check the service and try again.", () => submitMessage(message, { appendUser: false }));
  } finally {
    form.removeAttribute("aria-busy");
    input.disabled = false;
    sendButton.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  resizeInput();
  submitMessage(message);
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

input.addEventListener("input", resizeInput);