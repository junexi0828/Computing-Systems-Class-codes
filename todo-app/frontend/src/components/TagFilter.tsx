import React, { useState } from 'react';
import { Tag } from '../types';
import { tagApi } from '../services/api';
import { useNotification } from '../context/NotificationContext';
import { Plus, Tag as TagIcon, Palette } from 'lucide-react';

interface TagFilterProps {
  tags: Tag[];
  selectedTagId: string;
  onTagSelect: (tagId: string) => void;
  onCreateTag: () => void;
}

const TagFilter: React.FC<TagFilterProps> = ({
  tags,
  selectedTagId,
  onTagSelect,
  onCreateTag,
}) => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTagName, setNewTagName] = useState('');
  const [newTagColor, setNewTagColor] = useState('#3b82f6');
  const [isCreating, setIsCreating] = useState(false);
  
  const { addNotification } = useNotification();

  const handleCreateTag = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTagName.trim()) return;

    setIsCreating(true);
    try {
      await tagApi.createTag({
        name: newTagName.trim(),
        color: newTagColor,
      });
      
      setNewTagName('');
      setNewTagColor('#3b82f6');
      setShowCreateForm(false);
      onCreateTag();
      
      addNotification({
        type: 'success',
        message: '태그가 성공적으로 생성되었습니다!',
      });
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '태그 생성에 실패했습니다',
      });
    } finally {
      setIsCreating(false);
    }
  };

  const colorOptions = [
    { color: '#3b82f6', name: '파랑' },
    { color: '#ef4444', name: '빨강' },
    { color: '#10b981', name: '초록' },
    { color: '#f59e0b', name: '주황' },
    { color: '#8b5cf6', name: '보라' },
    { color: '#ec4899', name: '분홍' },
    { color: '#06b6d4', name: '청록' },
    { color: '#84cc16', name: '라임' },
  ];

  return (
    <div className="relative">
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2">
          <TagIcon className="h-4 w-4 text-gray-500" />
          <select
            value={selectedTagId}
            onChange={(e) => onTagSelect(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          >
            <option value="">모든 태그</option>
            {tags.map(tag => (
              <option key={tag.id} value={tag.id}>
                {tag.name}
              </option>
            ))}
          </select>
        </div>
        
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="flex items-center space-x-1 px-3 py-2 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors text-sm font-medium"
        >
          <Plus className="h-4 w-4" />
          <span className="hidden sm:block">태그 추가</span>
        </button>
      </div>

      {showCreateForm && (
        <div className="absolute top-full left-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg p-6 z-20 min-w-80">
          <div className="flex items-center space-x-2 mb-4">
            <Palette className="h-5 w-5 text-blue-600" />
            <h4 className="font-semibold text-gray-900">새 태그 만들기</h4>
          </div>
          
          <form onSubmit={handleCreateTag} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                태그 이름
              </label>
              <input
                type="text"
                value={newTagName}
                onChange={(e) => setNewTagName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="태그 이름을 입력하세요"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                색상 선택
              </label>
              <div className="grid grid-cols-4 gap-2">
                {colorOptions.map(({ color, name }) => (
                  <button
                    key={color}
                    type="button"
                    onClick={() => setNewTagColor(color)}
                    className={`w-full h-8 rounded-lg border-2 transition-all ${
                      newTagColor === color 
                        ? 'border-gray-800 scale-110' 
                        : 'border-gray-200 hover:border-gray-400'
                    }`}
                    style={{ backgroundColor: color }}
                    title={name}
                  />
                ))}
              </div>
            </div>
            
            <div className="flex justify-end space-x-2 pt-2">
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              >
                취소
              </button>
              <button
                type="submit"
                disabled={isCreating || !newTagName.trim()}
                className="px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCreating ? '생성 중...' : '생성'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default TagFilter;