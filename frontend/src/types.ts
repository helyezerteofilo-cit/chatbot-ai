export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  attachments?: MessageAttachment[];
}

export interface MessageAttachment {
  id: string;
  name: string;
  type: 'document';
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  documents?: UploadedDocument[];
}

export interface MessageRequest {
  message: string;
}

export interface MessageResponse {
  response: string;
  status: string;
  context?: Record<string, any>;
}

export interface UploadedDocument {
  id: string;
  name: string;
}

export interface DocumentUploadResponse {
  status: string;
  message: string;
  document_id?: string;
  document_name?: string;
}