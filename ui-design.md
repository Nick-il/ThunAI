<!DOCTYPE html><html lang="en" style=""><head><meta charset="utf-8"><meta content="width=device-width, initial-scale=1.0" name="viewport">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&amp;family=Inter:wght@400;500;600&amp;family=JetBrains+Mono:wght@400;500;600&amp;display=swap" rel="stylesheet">
<style>@layer base{html,body{margin:0;padding:0;}body{overscroll-behavior:none;}main>:first-child{margin-top:0!important;}main>:last-child{margin-bottom:0!important;}}::-webkit-scrollbar{display:none;}</style>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">tailwind.config = { 
  darkMode: "class", 
  theme: { 
    extend: { 
      colors: { 
        nordic: {
          bg: "#F8FAFC",
          card: "#FFFFFF",
          border: "#E2E8F0",
          borderStrong: "#CBD5E1",
          primary: "#0F172A",
          slate: "#1E293B",
          muted: "#475569",
          subtle: "#64748B",
          ice: "#F1F5F9",
          cobalt: "#2563EB",
          cobaltLight: "#3B82F6",
          codebg: "#0B1120"
        }
      },
      fontFamily: { 
        heading: ["Space Grotesk", "sans-serif"], 
        body: ["Inter", "sans-serif"], 
        mono: ["JetBrains Mono", "monospace"] 
      } 
    } 
  } 
};</script>
</head>
<body class="bg-[#F8FAFC] font-body text-[#0F172A] min-h-screen relative antialiased selection:bg-[#2563EB]/15 selection:text-[#2563EB]">
<!-- Sticky Minimal Frost Header -->
<header class="fixed top-0 left-0 w-full z-50 bg-[#F8FAFC]/85 backdrop-blur-md border-b border-[#E2E8F0] transition-colors duration-300">
<div class="max-w-[800px] h-14 mx-auto px-8 flex items-center justify-between">
<div class="flex items-center gap-2">
<span class="font-heading font-bold tracking-tight text-[16px] text-[#0F172A] select-none flex items-center gap-2">

        ThunAI
      </span>
</div>
<div class="flex items-center gap-2 font-mono text-[11px] text-[#64748B]">

</div>
</div>
</header>
<main class="relative z-10 w-full pt-14">
<div class="flex flex-col w-full">
<div class="relative w-full max-w-[800px] mx-auto px-8 pt-10 pb-32 flex flex-col min-h-[calc(100vh-3.5rem)]">
<!-- Query Bubble (User Prompt) -->
<div class="flex justify-end mb-10 w-full">
<div class="max-w-[620px] bg-white border border-[#E2E8F0] shadow-sm rounded-2xl px-5 py-4 text-left">
<p class="text-[15px] font-body leading-[24px] text-[#0F172A] select-text">Explain the architecture of modern AI memory systems with examples and benchmark comparison.</p>
</div>
</div>
<!-- AI Output Card / Continuous Clean Technical Document -->
<div class="w-full text-[#0F172A] select-text">
<div class="flex flex-wrap items-center gap-2 font-mono text-[12px] text-[#64748B] mb-3 pb-2 border-b border-[#E2E8F0] select-none tracking-tight"><span class="flex items-center gap-1.5 font-medium text-[#475569]"><span class="">thun-2.5-pro</span></span><span class="text-[#CBD5E1]">·</span><span class="">1,482 tokens</span><span class="text-[#CBD5E1]">·</span><span class="">1.4s</span></div><h1 class="font-heading text-[28px] font-bold leading-[36px] text-[#0F172A] mt-2 mb-4 tracking-[-0.025em]">Modern AI Memory Architectures</h1>
<p class="text-[16px] font-body leading-[26px] text-[#475569] mb-6">Retrieval-Augmented Generation (<strong class="font-semibold text-[#0F172A]">RAG</strong>) and external vector stores have become the standard pattern for providing long-term memory to large language models.</p>
<h2 class="font-heading text-[22px] font-bold leading-[30px] text-[#0F172A] mt-8 mb-3 tracking-[-0.015em] border-b border-[#E2E8F0] pb-2.5">Core Mechanisms</h2>
<ol class="list-decimal pl-6 space-y-2 mb-6 text-[16px] font-body leading-[26px] text-[#475569]">
<li class="">Query decomposition and semantic vector embedding.</li>
<li class="">Concurrent sparse-dense traversal over indexed memories (<code class="font-mono text-[13px] text-[#2563EB] px-1.5 py-0.5 rounded bg-[#F1F5F9] border border-[#E2E8F0]">HNSW</code> and <code class="font-mono text-[13px] text-[#2563EB] px-1.5 py-0.5 rounded bg-[#F1F5F9] border border-[#E2E8F0]">BM25</code>).</li>
<li class="">Recency-biased cross-attention injection into active transformer context.</li>
</ol>
<h3 class="font-heading text-[18px] font-semibold leading-[26px] text-[#0F172A] mt-6 mb-3 tracking-tight">Python Vector Pipeline Example</h3>
<!-- Code Block with 8px radius & 40px Header -->
<div class="rounded-lg border border-[#0F172A] bg-[#0B1120] my-5 overflow-hidden shadow-sm">
<div class="h-10 flex items-center justify-between px-4 bg-[#080D18] border-b border-white/10 text-[12px] font-mono text-[#94A3B8]">
<span class="tracking-wider text-[11px] uppercase font-semibold text-slate-400 flex items-center gap-2">
<span class="w-1.5 h-1.5 rounded-full bg-[#38BDF8]"></span>
              PYTHON
            </span>
<button class="text-[#94A3B8] hover:text-white transition-colors flex items-center gap-1.5 text-[12px] font-mono" id="copyCodeBtn">
<span class="material-symbols-outlined text-[15px]">content_copy</span>
<span class="">Copy</span>
</button>
</div>
<pre class="p-4 overflow-x-auto font-mono text-[13px] leading-[22px] text-[#E2E8F0] select-text"><code><span class="text-[#38BDF8] font-medium">import</span> numpy <span class="text-[#38BDF8] font-medium">as</span> np
<span class="text-[#38BDF8] font-medium">from</span> dataclasses <span class="text-[#38BDF8] font-medium">import</span> dataclass

<span class="text-[#818CF8]">@dataclass</span>
<span class="text-[#38BDF8] font-medium">class</span> <span class="text-[#E0F2FE] font-bold">MemoryStore</span>:
    embedding_dim: <span class="text-[#94A3B8]">int</span> = <span class="text-[#7DD3FC]">1536</span>
    decay_rate: <span class="text-[#94A3B8]">float</span> = <span class="text-[#7DD3FC]">0.985</span>

    <span class="text-[#38BDF8] font-medium">def</span> <span class="text-[#E0F2FE] font-medium">vector_cosine_sim</span>(self, query: np.ndarray, index: np.ndarray) -&gt; np.ndarray:
        norm_q = query / np.linalg.norm(query, axis=-<span class="text-[#7DD3FC]">1</span>, keepdims=<span class="text-[#38BDF8]">True</span>)
        norm_idx = index / np.linalg.norm(index, axis=-<span class="text-[#7DD3FC]">1</span>, keepdims=<span class="text-[#38BDF8]">True</span>)
        <span class="text-[#38BDF8] font-medium">return</span> np.dot(norm_idx, norm_q.T) * self.decay_rate</code></pre>
</div>
<h2 class="font-heading text-[22px] font-bold leading-[30px] text-[#0F172A] mt-8 mb-3 tracking-[-0.015em] border-b border-[#E2E8F0] pb-2.5">Benchmark Comparison</h2>
<!-- Clean 8px Radius Monospace Data Table -->
<div class="mt-4 mb-6 rounded-lg border border-[#E2E8F0] bg-white shadow-sm overflow-hidden">
<table class="w-full text-left font-body text-[14px] leading-[22px] border-collapse">
<thead>
<tr class="border-b border-[#E2E8F0] bg-[#F8FAFC] text-[#475569] text-[11px] font-mono uppercase tracking-wider">
<th class="py-3 px-4 font-semibold">Architecture</th>
<th class="py-3 px-4 text-right font-semibold">Retrieval Latency</th>
<th class="py-3 px-4 text-right font-semibold">Hallucination Rate</th>
<th class="py-3 px-4 text-right font-semibold">Context Window</th>
</tr>
</thead>
<tbody class="divide-y divide-[#E2E8F0] text-[#475569]">
<tr class="hover:bg-[#F1F5F9]/60 transition-colors">
<td class="py-3.5 px-4 text-[#0F172A] font-medium">Dense Vector (HNSW)</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">14ms</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">4.2%</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">128k tokens</td>
</tr>
<tr class="hover:bg-[#F1F5F9]/60 transition-colors">
<td class="py-3.5 px-4 text-[#0F172A] font-medium">Hybrid Sparse + Dense</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">22ms</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">1.8%</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">128k tokens</td>
</tr>
<tr class="hover:bg-[#F1F5F9]/60 transition-colors">
<td class="py-3.5 px-4 text-[#0F172A] font-medium">Recency Cross-Attention</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">38ms</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">1.1%</td>
<td class="py-3.5 px-4 text-right font-mono text-[13px] text-[#0F172A]">256k tokens</td>
</tr>
</tbody>
</table>
</div>
<!-- Glacial Cobalt Accented Callout / Blockquote with 3px border -->
<blockquote class="border-l-[3px] border-[#2563EB] bg-[#F1F5F9] rounded-r-lg px-5 py-3.5 my-6 text-[#1E293B] text-[15px] leading-[25px] italic">
          “Memory systems in autonomous agents must balance fast sparse lexical lookups with high-dimensional latent space representations to prevent degradation over long conversations.”
        </blockquote>
<h3 class="font-heading text-[18px] font-semibold leading-[26px] text-[#0F172A] mt-6 mb-3 tracking-tight">Key Takeaways</h3>
<ul class="list-disc pl-6 space-y-2 mb-4 text-[16px] font-body leading-[26px] text-[#475569]">
<li class="">Grounding context in verified vector stores minimizes catastrophic drift.</li>
<li class="">Sparse-dense hybrid search consistently outperforms raw semantic vectors on technical keywords.</li>
<li class="">For more details, explore the <a class="text-[#2563EB] hover:text-[#1D4ED8] hover:underline underline-offset-4 transition-colors font-medium" href="#">architecture documentation</a>.</li>
</ul>
</div>
<!-- Anchored Input Box Section with 16px radius & circular 40x40 cobalt send button -->
<div class="sticky bottom-6 w-full pt-8 z-30 max-w-[800px] mx-auto">
<div class="relative w-full rounded-2xl bg-white border border-[#CBD5E1] shadow-lg shadow-slate-200/50 p-3 transition-all focus-within:border-[#2563EB] focus-within:ring-2 focus-within:ring-[#2563EB]/15">
<textarea class="w-full bg-transparent border-0 outline-none focus:outline-none focus:ring-0 text-[#0F172A] placeholder:text-[#94A3B8] resize-none font-body text-[15px] leading-relaxed px-2 py-1" id="promptInput" placeholder="Ask anything…" rows="2"></textarea>
<div class="flex items-center justify-end pt-1">
<button class="w-10 h-10 rounded-full bg-[#2563EB] hover:bg-[#1D4ED8] text-white transition-all flex items-center justify-center shrink-0 active:scale-95 shadow-md shadow-[#2563EB]/25" id="sendBtn" type="button">
<span class="material-symbols-outlined text-[20px]">arrow_upward</span>
</button>
</div>
</div>
</div>
</div>
</div>
</main>
<!-- Interactive State Scripts -->
<script>
  const promptInput = document.getElementById('promptInput');
  const sendBtn = document.getElementById('sendBtn');
  const copyCodeBtn = document.getElementById('copyCodeBtn');

  if (promptInput) {
    promptInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (promptInput.value.trim().length > 0) {
          promptInput.value = '';
        }
      }
    });
  }

  if (sendBtn && promptInput) {
    sendBtn.addEventListener('click', () => {
      if (promptInput.value.trim().length > 0) {
        promptInput.value = '';
      }
    });
  }

  if (copyCodeBtn) {
    copyCodeBtn.addEventListener('click', () => {
      const originalHtml = copyCodeBtn.innerHTML;
      copyCodeBtn.innerHTML = `<span class="material-symbols-outlined text-[15px] text-[#38BDF8]">check</span><span class="text-[#38BDF8]">Copied</span>`;
      setTimeout(() => {
        copyCodeBtn.innerHTML = originalHtml;
      }, 1800);
    });
  }
</script>
</body></html>

