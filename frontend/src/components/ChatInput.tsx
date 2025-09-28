import { useState } from "react";

interface Props {
  onSubmit: (prompt: string) => void;
  isLoading: boolean;
}

export function ChatInput({ onSubmit, isLoading }: Props) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = prompt.trim();
    if (!trimmed) return;

    onSubmit(trimmed);
    setPrompt("");
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <textarea
        value={prompt}
        onChange={(event) => setPrompt(event.target.value)}
        placeholder="Ask anything about your knowledge base..."
        disabled={isLoading}
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? "Thinking..." : "Send"}
      </button>
    </form>
  );
}
