import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import apiClient from "../api/client.js";
import { useProject } from "../context/ProjectContext.jsx";

export default function ChatPage() {
  const { project, sessionId } = useProject();
  const [activeSessionId, setActiveSessionId] = useState(sessionId || null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending) return;

    setMessages((m) => [...m, { role: "user", text }]);
    setInput("");
    setSending(true);
    setError(null);

    try {
      const payload = {
        sessionId: activeSessionId || undefined,
        projectId: project?.projectId || undefined,
        question: text,
      };

      const { data } = await apiClient.post("/api/chatbot/query", payload);

      if (data.sessionId) setActiveSessionId(data.sessionId);

      const answer = data.answer || data.message || "No answer returned.";
      setMessages((m) => [...m, { role: "model", text: answer }]);
    } catch (err) {
      console.error("Chatbot request failed:", {
        url: err.config?.url,
        status: err.response?.status,
        response: err.response?.data,
        message: err.message,
        error: err,
      });
      setError("Something went wrong. Please try again.");
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="border-b border-slate-100 pb-3">
          <span className="border-b-2 border-[#D4AF37] pb-1 text-xs font-bold uppercase tracking-wider text-[#002B49]">
            AI Assistant
          </span>
        </div>

        <div className="mt-4 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[#002B49]">Ask SETU</h1>
            <p className="mt-2 text-sm text-slate-600">
              Ask about any project by name or code, filter by sector, state or risk, or ask why a project is at risk.
            </p>
          </div>

        </div>
      </section>

      <div className="h-[30rem] overflow-y-auto rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-4">
          {messages.length === 0 && (
            <p className="m-auto max-w-xs text-center text-sm text-slate-600">
              Try “Which road projects in Bihar are at high risk?” or “Why is this project delayed?”
            </p>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`max-w-[85%] ${m.role === "user" ? "self-end text-right" : "self-start"}`}>
              <p className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-slate-500">{m.role === "user" ? "You" : "SETU"}</p>

              <div
                className={`inline-block rounded-2xl px-4 py-3 text-sm text-left ${
                  m.role === "user"
                    ? "bg-[#002B49] text-white"
                    : "border border-slate-200 bg-[#FFFDF8] text-slate-700"
                }`}
              >
                <ReactMarkdown>{m.text}</ReactMarkdown>
              </div>
            </div>
          ))}

          {sending && <p className="self-start text-xs font-medium text-slate-500">SETU is thinking…</p>}
          <div ref={bottomRef} />
        </div>
      </div>

      {error && <p className="text-sm text-[#B42318]">{error}</p>}

      <form onSubmit={handleSend} className="flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question…"
          className="w-full rounded-lg border border-slate-200 bg-[#FFFDF8] px-4 py-3 text-sm text-slate-700 focus:border-[#D4AF37] focus:outline-none focus:ring-2 focus:ring-[#D4AF37]/20"
        />
        <button
          type="submit"
          disabled={sending}
          className="rounded-lg bg-[#002B49] px-6 py-3 text-sm font-bold text-white transition-colors hover:bg-[#163d63] disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
