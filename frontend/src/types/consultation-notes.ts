export interface ConsultationNotes {
  consultationId: string;
  notes: Note[];
  bookmarks: Bookmark[];
  highlights: Highlight[];
  followUps: FollowUp[];
  updatedAt: Date;
}

interface Note {
  id: string;
  type: 'general' | 'question' | 'chart' | 'timing' | 'recommendation';
  targetId?: string;
  content: string;
  author: string;
  createdAt: Date;
  updatedAt: Date;
  tags: string[];
  isPrivate: boolean;
}

interface Bookmark {
  id: string;
  targetType: 'report' | 'chapter' | 'question' | 'section';
  targetId: string;
  label: string;
  position: number;
  createdAt: Date;
}

interface Highlight {
  id: string;
  targetType: 'text' | 'evidence' | 'probability' | 'timing';
  targetId: string;
  content: string;
  color: string;
  note?: string;
  createdAt: Date;
}

interface FollowUp {
  id: string;
  title: string;
  description: string;
  dueDate?: Date;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  relatedQuestionId?: string;
  createdAt: Date;
  completedAt?: Date;
}

export interface NoteManager {
  addNote(note: Omit<Note, 'id' | 'createdAt' | 'updatedAt'>): Promise<Note>;
  updateNote(id: string, content: string): Promise<void>;
  deleteNote(id: string): Promise<void>;
  getNotes(consultationId: string): Promise<Note[]>;
  
  addBookmark(bookmark: Omit<Bookmark, 'id' | 'createdAt'>): Promise<Bookmark>;
  removeBookmark(id: string): Promise<void>;
  getBookmarks(consultationId: string): Promise<Bookmark[]>;
  
  addHighlight(highlight: Omit<Highlight, 'id' | 'createdAt'>): Promise<Highlight>;
  removeHighlight(id: string): Promise<void>;
  getHighlights(consultationId: string): Promise<Highlight[]>;
  
  addFollowUp(followUp: Omit<FollowUp, 'id' | 'createdAt'>): Promise<FollowUp>;
  updateFollowUp(id: string, updates: Partial<FollowUp>): Promise<void>;
  getFollowUps(consultationId: string): Promise<FollowUp[]>;
}