import React, { useState } from 'react';
import { Consultation, ConsultationStructure, Chapter, ChapterQuestion, ReportFormatting, ModeConfiguration, ReportFormatting } from '../../types/consultation';
import { ModeConfiguration, getModeConfig } from '../../types/report-modes';
import { QuestionPackage } from '../../types/packages';

interface ReportStructurePanelProps {
  consultation: any;
  onConsultationChange: (consultation: any) => void;
  modeConfig: any;
}

interface ChapterWithQuestions {
  id: string;
  title: string;
  order: number;
  included: boolean;
  customIntro?: string;
  questions: Array<{
    questionId: string;
    domainId: number;
    order: number;
    included: boolean;
    customLabel?: string;
  }>;
}

interface ReportStructurePanelProps {
  consultation: any;
  onConsultationChange: (consultation: any) => void;
  modeConfig: any;
}

export const ReportStructurePanel: React.FC<ReportStructurePanelProps> = ({
  consultation,
  onConsultationChange,
  modeConfig,
}) => {
  const [editingChapterId, setEditingChapterId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState('');
  const [editingIntro, setEditingIntro] = useState('');

  const chapters = consultation.structure?.chapters || [];

  const handleChapterToggle = (chapterId: string) => {
    const updatedChapters = consultation.structure.chapters.map((chapter: any) =>
      chapter.id === chapterId ? { ...chapter, included: !chapter.included } : chapter
    );
    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: updatedChapters },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  };

  const handleQuestionToggle = (chapterId: string, questionId: string) => {
    const updatedChapters = consultation.structure.chapters.map((chapter: any) =>
      chapter.id === chapterId
        ? {
            ...chapter,
            questions: chapter.questions.map((q: any) =>
              q.questionId === questionId ? { ...q, included: !q.included } : q
            ),
          }
        : chapter
    );
    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: updatedChapters },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  });

  const handleChapterTitleChange = (chapterId: string, newTitle: string) => {
    const updatedChapters = consultation.structure.chapters.map((chapter: any) =>
      chapter.id === chapterId ? { ...chapter, title: newTitle } : chapter
    );
    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: updatedChapters },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  };

  const handleIntroChange = (chapterId: string, intro: string) => {
    const updatedChapters = consultation.structure.chapters.map((chapter: any) =>
      chapter.id === chapterId ? { ...chapter, customIntro: intro } : chapter
    );
    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: updatedChapters },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  };

  const handleAddChapter = () => {
    const newChapter = {
      id: `chapter-${Date.now()}`,
      title: 'New Chapter',
      order: consultation.structure.chapters.length + 1,
      included: true,
      customIntro: '',
      questions: [],
    };
    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: [...consultation.structure.chapters, newChapter] },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  };

  const handleReorder = (fromIndex: number, toIndex: number) => {
    const newChapters = [...consultation.structure.chapters];
    const [removed] = newChapters.splice(fromIndex, 1);
    newChapters.splice(toIndex, 0, removed);
    
    const updatedChapters = newChapters.map((chapter, index) => ({
      ...chapter,
      order: index + 1,
    }));
    
    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: updatedChapters },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  };

  const handleDeleteChapter = (chapterId: string) => {
    if (window.confirm('Are you sure you want to delete this chapter?')) {
      const updatedChapters = consultation.structure.chapters
        .filter((c: any) => c.id !== chapterId)
        .map((chapter, index) => ({ ...chapter, order: index + 1 }));
      onConsultationChange({
        ...consultation,
        structure: { ...consultation.structure, chapters: updatedChapters },
        metadata: { ...consultation.metadata, updatedAt: new Date() },
      });
    }
  };

  const handleQuestionReorder = (chapterId: string, fromIndex: number, toIndex: number) => {
    const chapter = consultation.structure.chapters.find((c: any) => c.id === chapterId);
    if (!chapter) return;
    
    const newQuestions = [...chapter.questions];
    const [removed] = newQuestions.splice(fromIndex, 1);
    newQuestions.splice(toIndex, 0, removed);
    
    const updatedChapters = consultation.structure.chapters.map((chapter: any) =>
      chapter.id === chapterId
        ? { ...chapter, questions: newQuestions.map((q, index) => ({ ...q, order: index + 1 })) }
        : chapter
    );
    
    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: updatedChapters },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  };

  const estimatedPages = useMemo(() => {
    let total = 0;
    consultation.structure.chapters.forEach((chapter: any) => {
      if (chapter.included) {
        chapter.questions.forEach((q: any) => {
          if (q.included) total += 1.2;
        });
      }
    });
    return Math.ceil(total + 3); // +3 for cover, TOC, executive summary
  }, [consultation.structure.chapters]);

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Toolbar */}
      <div className="p-4 border-b border-gray-200 bg-gray-50 flex flex-wrap gap-2">
        <button
          onClick={handleAddChapter}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm font-medium"
        >
          + Add Chapter
        </button>
        <div className="flex-1"></div>
        <div className="text-sm text-gray-600">
          Estimated: {estimatedPages} pages
        </div>
      </div>

      {/* Chapters List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {consultation.structure?.chapters?.map((chapter: any, chapterIndex: number) => (
          <ChapterCard
            key={chapter.id}
            chapter={chapter}
            chapterIndex={chapterIndex}
            isEditing={editingChapterId === chapter.id}
            editingTitle={editingTitle}
            setEditingTitle={setEditingTitle}
            editingIntro={editingIntro}
            setEditingIntro={setEditingIntro}
            editingChapterId={editingChapterId}
            setEditingChapterId={setEditingChapterId}
            onToggle={handleChapterToggle}
            onTitleChange={handleChapterTitleChange}
            onIntroChange={handleIntroChange}
            onReorder={handleReorder}
            onDelete={handleDeleteChapter}
            onQuestionToggle={handleQuestionToggle}
            onQuestionReorder={handleQuestionReorder}
            chapterIndex={chapterIndex}
            totalChapters={consultation.structure.chapters.length}
            modeConfig={modeConfig}
          />
        ))}
        
        {(!consultation.structure?.chapters?.length) && (
          <div className="text-center py-12 text-gray-400">
            <p className="text-lg font-medium">No chapters yet</p>
            <p className="text-sm text-gray-500 mt-2">Click "Add Chapter" to start building your consultation report</p>
          </div>
        )}
      </div>
    </div>
  );
};

interface ChapterCardProps {
  chapter: any;
  chapterIndex: number;
  isEditing: boolean;
  editingTitle: string;
  setEditingTitle: (title: string) => void;
  editingIntro: string;
  setEditingIntro: (intro: string) => void;
  editingChapterId: string | null;
  setEditingChapterId: (id: string | null) => void;
  onToggle: (chapterId: string) => void;
  onTitleChange: (chapterId: string, title: string) => void;
  onIntroChange: (chapterId: string, intro: string) => void;
  onReorder: (fromIndex: number, toIndex: number) => void;
  onDelete: (chapterId: string) => void;
  onQuestionToggle: (chapterId: string, questionId: string) => void;
  onQuestionReorder: (chapterId: string, fromIndex: number, toIndex: number) => void;
  chapterIndex: number;
  totalChapters: number;
  modeConfig: any;
}

const ChapterCard: React.FC<ChapterCardProps> = ({
  chapter,
  chapterIndex,
  isEditing,
  editingTitle,
  setEditingTitle,
  editingIntro,
  setEditingIntro,
  editingChapterId,
  setEditingChapterId,
  onToggle,
  onTitleChange,
  onIntroChange,
  onReorder,
  onDelete,
  onQuestionToggle,
  onQuestionReorder,
  chapterIndex,
  totalChapters,
  modeConfig,
}) => {
  const includedQuestions = chapter.questions?.filter((q: any) => q.included).length || 0;
  const totalQuestions = chapter.questions?.length || 0;

  const handleDragStart = (e: React.DragEvent, index: number) => {
    e.dataTransfer.setData('text/plain', index.toString());
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e: React.DragEvent, targetIndex: number) => {
    e.preventDefault();
    const fromIndex = parseInt(e.dataTransfer.getData('text/plain'));
    if (fromIndex !== targetIndex) {
      // This would be handled by the parent
    }
  };

  return (
    <div 
      className={`bg-white border rounded-lg shadow-sm ${isEditing ? 'ring-2 ring-blue-200' : ''}`}
      draggable
      onDragStart={(e) => {}}
      onDragOver={(e) => e.preventDefault()}
      onDrop={() => {}}
    >
      {/* Chapter Header */}
      <div className="p-4 border-b border-gray-100 bg-gray-50 flex items-center gap-3">
        <input
          type="checkbox"
          checked={chapter.included}
          onChange={() => {}}
          className="form-checkbox h-5 w-5 text-blue-600"
        />
        
        {isEditing ? (
          <input
            type="text"
            value={editingTitle}
            onChange={(e) => {}}
            className="flex-1 px-3 py-1 border border-blue-300 rounded text-sm font-medium focus:ring-2 focus:ring-blue-500"
            autoFocus
          />
        ) : (
          <h3 className="flex-1 font-medium text-gray-800">{chapter.title}</h3>
        )}
        
        <span className="text-sm text-gray-500">
          {chapter.questions?.filter((q: any) => q.included).length || 0} / {chapter.questions?.length || 0} questions
        </span>
        
        <div className="flex items-center gap-1 ml-auto">
          {chapterIndex > 0 && (
            <button
              className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100"
              title="Move up"
            >
              ↑
            </button>
          )}
          {chapterIndex < 9 && (
            <button
              className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100"
              title="Move down"
            >
              ↓
            </button>
          )}
          <button
            onClick={() => {}}
            className="p-1 text-gray-400 hover:text-blue-600 rounded hover:bg-gray-100"
            title="Edit chapter"
          >
            ✏️
          </button>
          <button
            className="p-1 text-gray-400 hover:text-red-600 rounded hover:bg-gray-100"
            title="Delete chapter"
          >
            🗑️
          </button>
        </div>
      </div>

      {/* Chapter Intro */}
      {chapter.customIntro && (
        <div className="p-4 border-b border-gray-100 bg-gray-50 text-sm text-gray-600 italic">
          {chapter.customIntro}
        </div>
      )}

      {/* Questions List */}
      <div className="divide-y divide-gray-100">
        {chapter.questions?.map((question: any, qIndex: number) => (
          <div key={question.questionId} className="px-4 py-3 hover:bg-gray-50 flex items-center gap-3">
            <input
              type="checkbox"
              checked={question.included}
              onChange={() => {}}
              className="form-checkbox h-4 w-4 text-blue-600"
            />
            <span className="flex-1 text-sm text-gray-700">{question.customLabel || `Question ${question.questionId}`}</span>
            <span className="text-xs text-gray-400">{question.domainId}</span>
            <button className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100" title="Move question">
              ⋮⋮
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReportStructurePanel;