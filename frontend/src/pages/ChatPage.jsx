import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import apiClient from "../api/client.js";
import { useProject } from "../context/ProjectContext.jsx";

export default function ChatPage() {
  const { project, sessionId } = useProject();
  const [useProjectContext, setUseProjectContext] = useState(Boolean(project));
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

    if (!sessionId) {
      setError("Please predict a project first so a chat session can be created.");
      return;
    }

    const priorHistory = messages;
    setMessages((m) => [...m, { role: "user", text }]);
    setInput("");
    setSending(true);
    setError(null);

    try {
      const { data } = await apiClient.post("/api/chat", {
        session_id: sessionId,
        message: text,
      });
      setMessages((m) => [...m, { role: "model", text: data.answer }]);
    } catch (err) {
      setError(err.response?.data?.detail || "Couldn't reach SETU. Is the chatbot API running?");
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="font-display text-3xl">Ask SETU</h1>
          <p className="mt-2 text-sm text-steel">
            Ask about any project by name or code, filter by sector, state or risk, or ask why a project is at risk.
          </p>
        </div>

        {project && (
          <button
            type="button"
            onClick={() => setUseProjectContext((prev) => !prev)}
            className={`inline-flex items-center justify-center rounded-full border px-3 py-1.5 text-xs font-medium transition-colors ${
              useProjectContext
                ? "border-ink bg-ink text-paper"
                : "border-ink/20 bg-white/60 text-ink hover:border-ink/40"
            }`}
          >
            {useProjectContext ? `Focused on ${project.project_name}` : "Focus on this project"}
          </button>
        )}
      </div>

      <div className="mt-8 border border-ink/15 bg-white/40 h-[30rem] overflow-y-auto p-5 flex flex-col gap-4 rounded-3xl">
        {messages.length === 0 && (
          <p className="text-sm text-steel m-auto text-center max-w-xs">
            Try “Which road projects in Bihar are at high risk?” or “Why is this project delayed?”
          </p>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`max-w-[85%] ${m.role === "user" ? "self-end text-right" : "self-start"}`}>
            <p className="text-[10px] text-steel mb-1">{m.role === "user" ? "You" : "SETU"}</p>

            <div
              className={`inline-block rounded-2xl px-4 py-3 text-sm text-left ${
                m.role === "user"
                  ? "bg-ink text-paper"
                  : "border border-ink/15 bg-paper/80 markdown-content"
              }`}
            >
              <ReactMarkdown>{m.text}</ReactMarkdown>
            </div>
          </div>
        ))}

        {sending && <p className="text-xs text-steel self-start">SETU is thinking…</p>}
        <div ref={bottomRef} />
      </div>

      {error && <p className="mt-3 text-sm text-brick">{error}</p>}

      <form onSubmit={handleSend} className="mt-4 flex gap-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question…"
          className="field-input flex-1 rounded-2xl"
        />
        <button
          type="submit"
          disabled={sending}
          className="rounded-full bg-ink px-6 py-3 text-sm font-medium text-paper transition-colors hover:bg-blueprint disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
