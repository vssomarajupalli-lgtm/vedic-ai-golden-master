import React, { useState, useMemo } from 'react';

interface ReportStructurePanelProps {
  consultation: any;
  onConsultationChange: (consultation: any) => void;
}

export const ReportStructurePanel: React.FC<ReportStructurePanelProps> = ({
  consultation,
  onConsultationChange,
}) => {
  const [editingChapterId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState('');

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

  const handleDeleteChapter = (chapterId: string) => {
    if (window.confirm('Are you sure you want to delete this chapter?')) {
      const updatedChapters = consultation.structure.chapters
        .filter((c: any) => c.id !== chapterId)
        .map((chapter: any, index: number) => ({ ...chapter, order: index + 1 }));
      onConsultationChange({
        ...consultation,
        structure: { ...consultation.structure, chapters: updatedChapters },
        metadata: { ...consultation.metadata, updatedAt: new Date() },
      });
    }
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
    return Math.ceil(total + 3);
  }, [consultation.structure.chapters]);

  const handleChapterReorder = (fromIndex: number, toIndex: number) => {
    const newChapters = [...consultation.structure.chapters];
    const [removed] = newChapters.splice(fromIndex, 1);
    newChapters.splice(toIndex, 0, removed);

    const updatedChapters = newChapters.map((chapter: any, index: number) => ({
      ...chapter,
      order: index + 1,
    }));

    onConsultationChange({
      ...consultation,
      structure: { ...consultation.structure, chapters: updatedChapters },
      metadata: { ...consultation.metadata, updatedAt: new Date() },
    });
  };

  return (
    <div className="h-full flex flex-col bg-white">
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

      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {consultation.structure?.chapters?.map((chapter: any, chapterIdx: number) => (
          <ChapterCard
            key={chapter.id}
            chapter={chapter}
            chapterIdx={chapterIdx}
            isEditing={editingChapterId === chapter.id}
            editingTitle={editingTitle}
            setEditingTitle={setEditingTitle}
            onToggle={handleChapterToggle}
            onReorder={handleChapterReorder}
            onDelete={handleDeleteChapter}
            onQuestionToggle={handleQuestionToggle}
            totalChapters={consultation.structure.chapters.length}
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

const ChapterCard: React.FC<{
  chapter: any;
  chapterIdx: number;
  isEditing: boolean;
  editingTitle: string;
  setEditingTitle: (title: string) => void;
  onToggle: (chapterId: string) => void;
  onReorder: (fromIndex: number, toIndex: number) => void;
  onDelete: (chapterId: string) => void;
  onQuestionToggle: (chapterId: string, questionId: string) => void;
  totalChapters: number;
}> = ({
  chapter,
  chapterIdx,
  isEditing,
  editingTitle,
  setEditingTitle,
  onToggle,
  onReorder,
  onDelete,
  onQuestionToggle,
  totalChapters,
}) => {
  return (
    <div
      className={`bg-white border rounded-lg shadow-sm ${isEditing ? 'ring-2 ring-blue-200' : ''}`}
      draggable
      onDragStart={(e) => {
        e.dataTransfer.setData('text/plain', chapterIdx.toString());
        e.dataTransfer.effectAllowed = 'move';
      }}
      onDragOver={(e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
      }}
      onDrop={() => {}}
    >
      <div className="p-4 border-b border-gray-100 bg-gray-50 flex items-center gap-3">
        <input
          type="checkbox"
          checked={chapter.included}
          onChange={() => onToggle(chapter.id)}
          className="form-checkbox h-5 w-5 text-blue-600"
        />

        {isEditing ? (
          <input
            type="text"
            value={editingTitle}
            onChange={(e) => setEditingTitle(e.target.value)}
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
          {chapterIdx > 0 && (
            <button
              onClick={() => onReorder(chapterIdx, chapterIdx - 1)}
              className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100"
              title="Move up"
            >
              Up
            </button>
          )}
          {chapterIdx < totalChapters - 1 && (
            <button
              onClick={() => onReorder(chapterIdx, chapterIdx + 1)}
              className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100"
              title="Move down"
            >
              Down
            </button>
          )}
          <button
            onClick={() => {}}
            className="p-1 text-gray-400 hover:text-blue-600 rounded hover:bg-gray-100"
            title="Edit chapter"
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(chapter.id)}
            className="p-1 text-gray-400 hover:text-red-600 rounded hover:bg-gray-100"
            title="Delete chapter"
          >
            Delete
          </button>
        </div>
      </div>

      {chapter.customIntro && (
        <div className="p-4 border-b border-gray-100 bg-gray-50 text-sm text-gray-600 italic">
          {chapter.customIntro}
        </div>
      )}

      <div className="divide-y divide-gray-100">
        {chapter.questions?.map((question: any, qIdx: number) => (
          <div key={question.questionId} className="px-4 py-3 hover:bg-gray-50 flex items-center gap-3">
            <input
              type="checkbox"
              checked={question.included}
              onChange={() => onQuestionToggle(chapter.id, question.questionId)}
              className="form-checkbox h-4 w-4 text-blue-600"
            />
            <span className="flex-1 text-sm text-gray-700">{question.customLabel || `Question ${question.questionId}`}</span>
            <span className="text-xs text-gray-400">{question.domainId}</span>
            <button
              onClick={() => {}}
              disabled={qIdx >= (chapter.questions?.length || 1) - 1}
              className="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100 disabled:opacity-50"
              title="Move question"
            >
              Move
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReportStructurePanel;