import { useState, useRef, useEffect } from "react";
import axios from "axios";

// Point this at your own backend/chat endpoint.
// Expected request:  { message: string }
// Expected response: { reply: string }
const API_URL = "http://127.0.0.1:8000";

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { id: 1, sender: "bot", text: "Hey! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    const userMessage = { id: Date.now(), sender: "user", text: trimmed };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const data = await axios.post(API_URL + "/userquery", { user_query: trimmed });
      console.log(data.data.reply)
      const botMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text: data.data.reply,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text: "Sorry, something went wrong reaching the server. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !isLoading) sendMessage();
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-slate-100 p-4">
      <div className="flex h-150 w-full max-w-md flex-col overflow-hidden rounded-2xl bg-white shadow-xl">
        {/* Header */}
        <div className="bg-slate-800 px-4 py-3">
          <h1 className="text-lg font-semibold text-white">Chatbot</h1>
        </div>

        {/* Messages */}
        <div className="flex-1 space-y-3 overflow-y-auto bg-slate-50 p-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-2 text-sm leading-relaxed ${
                  msg.sender === "user"
                    ? "rounded-br-sm bg-slate-800 text-white"
                    : "rounded-bl-sm bg-white text-slate-800 shadow"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[75%] rounded-2xl rounded-bl-sm bg-white px-4 py-2 text-sm text-slate-400 shadow">
                Typing...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="flex items-center gap-2 border-t border-slate-200 bg-white p-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message..."
            disabled={isLoading}
            className="flex-1 rounded-full border border-slate-300 px-4 py-2 text-sm outline-none focus:border-slate-500 disabled:opacity-60"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading}
            className="rounded-full bg-slate-800 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:opacity-60"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}