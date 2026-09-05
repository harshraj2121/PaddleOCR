import { useState, useRef, useEffect } from "react";
import axios from "axios";

export default function Chatbot() {
  const backend_url = import.meta.env.VITE_API_URL;
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
      const data = await axios.post(backend_url + "/userquery", { user_query: trimmed });
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
    <div className="min-h-screen flex flex-col gap-4 w-full items-center justify-center bg-slate-950 p-4 relative overflow-hidden">

      {/* Background decoration */}
      <div className="absolute -top-37.5 -left-37.5 w-100 h-100 bg-blue-600/20 rounded-full blur-3xl" />
      {/* <div className="absolute -bottom-37.5 -right-37.5 w-100 h-100 bg-purple-600/20 rounded-full blur-3xl" /> */}

      <nav className="w-full max-w-md h-10 flex items-center justify-center gap-3">
        <a href="/chat" className="bg-linear-45 from-violet-900 to-blue-500 px-10 py-2 rounded-full text-white font-semibold cursor-pointer">Chat</a>
        <a href="/upload" className="bg-linear-45 from-violet-900 to-blue-500 px-10 py-2 rounded-full text-white font-semibold cursor-pointer">Upload</a>
      </nav>

      <div className="flex h-145 w-full max-w-xl flex-col overflow-hidden rounded-2xl bg-gray-800 shadow-xl">
        <div className="bg-gray-700 px-4 py-3">
          <h1 className="text-lg font-semibold text-white">Chatbot</h1>
        </div>

       <div className="flex-1 space-y-3 overflow-y-auto bg-gray-800 p-4">
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
                    ? "rounded-br-sm bg-blue-600 text-white"
                    : "rounded-bl-sm bg-gray-700 text-gray-200 shadow"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[75%] rounded-2xl rounded-bl-sm bg-gray-700 px-4 py-2 text-sm text-gray-400 shadow">
                Typing...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="flex items-center gap-2 border-t border-gray-700 bg-gray-800 p-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message..."
            disabled={isLoading}
            className="flex-1 rounded-full border border-gray-600 bg-gray-900 px-4 py-2 text-sm text-gray-200 outline-none focus:border-blue-500 disabled:opacity-60"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading}
            className="rounded-full bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-500 disabled:opacity-60"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
