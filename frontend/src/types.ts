export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

export interface MessageRequest {
  message: string;
}

export interface MessageResponse {
  response: string;
  status: string;
  context?: Record<string, any>;
}
