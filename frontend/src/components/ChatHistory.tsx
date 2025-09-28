import type { ChatResponse } from "../types";

interface Props {
  history: ChatResponse[];
  isLoading: boolean;
}

export function ChatHistory({ history, isLoading }: Props) {
  if (history.length === 0 && !isLoading) {
    return <p className="placeholder">Start chatting to see responses here.</p>;
  }

  return (
    <section className="chat-history">
      {history.map((item, index) => (
        <article key={index} className="chat-message">
          <div className="chat-response">{item.response}</div>
          {item.sources.length > 0 && (
            <ul className="chat-sources">
              {item.sources.map((source, sourceIndex) => (
                <li key={sourceIndex}>{source}</li>
              ))}
            </ul>
          )}
        </article>
      ))}
      {isLoading && <p className="loading">Generating response...</p>}
    </section>
  );
}
