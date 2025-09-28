import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";

import type { ChatRequest, ChatResponse } from "./types";
import { ChatHistory } from "./components/ChatHistory";
import { ChatInput } from "./components/ChatInput";

export default function App() {
  const [history, setHistory] = useState<ChatResponse[]>([]);

  const mutation = useMutation({
    mutationFn: async (payload: ChatRequest) => {
      const response = await axios.post<ChatResponse>("/api/chat/query", payload);
      return response.data;
    },
    onSuccess: (data) => {
      setHistory((prev) => [...prev, data]);
    },
  });

  const handleSubmit = (prompt: string) => {
    mutation.mutate({ prompt, top_k: 5, stream: false });
  };

  return (
    <div className="app-container">
      <header>
        <h1>AI Browser Chat</h1>
      </header>
      <main>
        <ChatHistory history={history} isLoading={mutation.isPending} />
      </main>
      <footer>
        <ChatInput onSubmit={handleSubmit} isLoading={mutation.isPending} />
      </footer>
    </div>
  );
}
