export interface ChatRequest {
  prompt: string;
  top_k?: number;
  stream?: boolean;
}

export interface ChatResponse {
  response: string;
  sources: string[];
}
