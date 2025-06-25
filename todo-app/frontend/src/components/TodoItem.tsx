import React, { useState } from 'react';
import { Todo, Tag } from '../types';
import { Check, Edit2, Trash2, Save, X, Calendar, Flag } from 'lucide-react';

interface TodoItemProps {
  todo: Todo;
  tags: Tag[];
  onUpdate: (id: string, updates: Partial<Todo>) => void;
  onDelete: (id: string) => void;
  onToggleComplete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  tags,
  onUpdate,
  onDelete,
  onToggleComplete,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    title: todo.title,
    description: todo.description || '',
    priority: todo.priority,
    tagId: todo.tagId || '',
  });

  const handleSave = () => {
    onUpdate(todo.id, {
      title: editData.title,
      description: editData.description || undefined,
      priority: editData.priority,
      tagId: editData.tagId || undefined,
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditData({
      title: todo.title,
      description: todo.description || '',
      priority: todo.priority,
      tagId: todo.tagId || '',
    });
    setIsEditing(false);
  };

  const getPriorityConfig = (priority: string) => {
    switch (priority) {
      case 'high':
        return {
          color: 'bg-red-100 text-red-800 border-red-200',
          label: '높음',
          icon: '🔴'
        };
      case 'medium':
        return {
          color: 'bg-yellow-100 text-yellow-800 border-yellow-200',
          label: '보통',
          icon: '🟡'
        };
      case 'low':
        return {
          color: 'bg-green-100 text-green-800 border-green-200',
          label: '낮음',
          icon: '🟢'
        };
      default:
        return {
          color: 'bg-gray-100 text-gray-800 border-gray-200',
          label: '보통',
          icon: '⚪'
        };
    }
  };

  const getTagInfo = (tagId: string) => {
    return tags.find(tag => tag.id === tagId);
  };

  const tag = todo.tagId ? getTagInfo(todo.tagId) : null;
  const priorityConfig = getPriorityConfig(todo.priority);

  return (
    <div className={`bg-white rounded-xl border shadow-sm transition-all duration-200 hover:shadow-md ${
      todo.completed ? 'opacity-75 bg-gray-50' : ''
    }`}>
      <div className="p-6">
        {isEditing ? (
          <div className="space-y-4">
            <input
              type="text"
              value={editData.title}
              onChange={(e) => setEditData({ ...editData, title: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-medium"
              placeholder="할 일 제목"
            />
            
            <textarea
              value={editData.description}
              onChange={(e) => setEditData({ ...editData, description: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              placeholder="설명 (선택사항)"
              rows={2}
            />
            
            <div className="flex flex-col sm:flex-row gap-3">
              <select
                value={editData.priority}
                onChange={(e) => setEditData({ ...editData, priority: e.target.value as Todo['priority'] })}
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="low">낮은 우선순위</option>
                <option value="medium">보통 우선순위</option>
                <option value="high">높은 우선순위</option>
              </select>
              
              <select
                value={editData.tagId}
                onChange={(e) => setEditData({ ...editData, tagId: e.target.value })}
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">태그 없음</option>
                {tags.map(tag => (
                  <option key={tag.id} value={tag.id}>{tag.name}</option>
                ))}
              </select>
            </div>
            
            <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
              <button
                onClick={handleCancel}
                className="flex items-center space-x-2 px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="h-4 w-4" />
                <span>취소</span>
              </button>
              <button
                onClick={handleSave}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-lg transition-colors"
              >
                <Save className="h-4 w-4" />
                <span>저장</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="flex items-start space-x-4">
            <button
              onClick={() => onToggleComplete(todo.id)}
              className={`flex-shrink-0 mt-1 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-200 ${
                todo.completed
                  ? 'bg-green-500 border-green-500 text-white shadow-md'
                  : 'border-gray-300 hover:border-green-400 hover:bg-green-50'
              }`}
            >
              {todo.completed && <Check className="h-4 w-4" />}
            </button>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className={`font-semibold text-lg mb-2 ${
                    todo.completed ? 'line-through text-gray-500' : 'text-gray-900'
                  }`}>
                    {todo.title}
                  </h3>
                  
                  {todo.description && (
                    <p className={`text-sm mb-3 leading-relaxed ${
                      todo.completed ? 'line-through text-gray-400' : 'text-gray-600'
                    }`}>
                      {todo.description}
                    </p>
                  )}
                  
                  <div className="flex items-center flex-wrap gap-2">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${priorityConfig.color}`}>
                      <span className="mr-1">{priorityConfig.icon}</span>
                      {priorityConfig.label}
                    </span>
                    
                    {tag && (
                      <span
                        className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium text-white shadow-sm"
                        style={{ backgroundColor: tag.color }}
                      >
                        {tag.name}
                      </span>
                    )}
                    
                    <span className="inline-flex items-center text-xs text-gray-500">
                      <Calendar className="h-3 w-3 mr-1" />
                      {new Date(todo.createdAt).toLocaleDateString('ko-KR')}
                    </span>
                  </div>
                </div>
                
                <div className="flex items-center space-x-1 ml-4">
                  <button
                    onClick={() => setIsEditing(true)}
                    className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="수정"
                  >
                    <Edit2 className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => onDelete(todo.id)}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="삭제"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TodoItem;