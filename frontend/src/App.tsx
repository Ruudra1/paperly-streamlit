import React, { useMemo, useState } from 'react'
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/react'

type ChatMessage = { role: 'user' | 'assistant'; content: string }

const API_BASE = (import.meta as any).env?.VITE_API_BASE ?? 'http://127.0.0.1:8080'

export default function App() {
  const [file, setFile] = useState<File | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [processing, setProcessing] = useState(false)
  const [processingStatus, setProcessingStatus] = useState<string>('')

  const [summary, setSummary] = useState<string | null>(null)
  const [summarizing, setSummarizing] = useState(false)

  const [question, setQuestion] = useState('')
  const [chat, setChat] = useState<ChatMessage[]>([])
  const [asking, setAsking] = useState(false)

  const canSummarizeOrChat = useMemo(() => Boolean(sessionId), [sessionId])

  async function processPaper() {
    if (!file) return
    setProcessing(true)
    setProcessingStatus('Uploading PDF...')
    setSummary(null)
    setChat([])

    try {
      const form = new FormData()
      form.append('file', file)

      setProcessingStatus('Processing PDF and extracting text...')
      const res = await fetch(`${API_BASE}/api/process`, {
        method: 'POST',
        body: form
      })

      if (!res.ok) {
        const err = await res.json().catch(() => null)
        throw new Error(err?.detail ?? `Process failed (${res.status})`)
      }

      setProcessingStatus('Building vector index...')
      const data = (await res.json()) as { session_id: string }
      setSessionId(data.session_id)
      setProcessingStatus('Ready!')
    } catch (e: any) {
      setProcessingStatus('Failed')
      alert(e?.message ?? String(e))
    } finally {
      setProcessing(false)
    }
  }

  async function summarize() {
    if (!sessionId) return
    setSummarizing(true)
    setSummary(null)

    try {
      const res = await fetch(`${API_BASE}/api/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
      })

      if (!res.ok) {
        const err = await res.json().catch(() => null)
        throw new Error(err?.detail ?? `Summarize failed (${res.status})`)
      }

      const data = (await res.json()) as { summary: string }
      setSummary(data.summary)
    } catch (e: any) {
      alert(e?.message ?? String(e))
    } finally {
      setSummarizing(false)
    }
  }

  async function ask() {
    if (!sessionId) return
    const q = question.trim()
    if (!q) return

    setAsking(true)
    setQuestion('')
    setChat((prev) => [...prev, { role: 'user', content: q }])

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, question: q })
      })

      if (!res.ok) {
        const err = await res.json().catch(() => null)
        throw new Error(err?.detail ?? `Chat failed (${res.status})`)
      }

      const data = (await res.json()) as { answer: string }
      setChat((prev) => [...prev, { role: 'assistant', content: data.answer }])
    } catch (e: any) {
      alert(e?.message ?? String(e))
    } finally {
      setAsking(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <div className="title">Paperly</div>
        <div className="subtitle">Upload a PDF research paper, then summarize or chat with it (RAG + Groq Llama 70B).</div>
      </header>

      <section className="card">
        <div className="sectionTitle">1) Upload</div>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <div className="row">
          <button className="btn" disabled={!file || processing} onClick={processPaper}>
            {processing ? 'Processing…' : 'Process Paper'}
          </button>
          <div className="muted">
            {sessionId ? `Session: ${sessionId}` : 'No active session yet'}
          </div>
        </div>
        {processing && (
          <div className="progress">
            <div className="progressBar">
              <div className="progressFill" />
            </div>
            <div className="progressText">{processingStatus}</div>
          </div>
        )}
      </section>

      <section className="grid">
        <div className="card">
          <div className="sectionTitle">2) Summarize</div>
          <button className="btn" disabled={!canSummarizeOrChat || summarizing} onClick={summarize}>
            {summarizing ? 'Summarizing…' : 'Summarize'}
          </button>
          {summary && (
            <div className="output">
              <div className="outputTitle">Summary</div>
              <pre className="pre">{summary}</pre>
            </div>
          )}
        </div>

        <div className="card">
          <div className="sectionTitle">3) Chat</div>
          <div className="chat">
            {chat.length === 0 ? (
              <div className="muted">Ask something after you process a paper.</div>
            ) : (
              chat.map((m, idx) => (
                <div key={idx} className={`msg ${m.role}`}>
                  <div className="role">{m.role === 'user' ? 'You' : 'Paperly'}</div>
                  <div className="content">{m.content}</div>
                </div>
              ))
            )}
          </div>
          <div className="row">
            <input
              className="input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about the paper…"
              disabled={!canSummarizeOrChat || asking}
              onKeyDown={(e) => {
                if (e.key === 'Enter') ask()
              }}
            />
            <button className="btn" disabled={!canSummarizeOrChat || asking} onClick={ask}>
              {asking ? 'Sending…' : 'Send'}
            </button>
          </div>
        </div>
      </section>

      <footer className="footer">
        Backend: {API_BASE}
      </footer>
      <Analytics />
      <SpeedInsights />
    </div>
  )
}
