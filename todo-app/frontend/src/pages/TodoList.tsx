import React, { useState, useEffect } from 'react';
import { useNotification } from '../context/NotificationContext';
import { todoApi, tagApi } from '../services/api';
import { Todo, Tag } from '../types';
import TodoItem from '../components/TodoItem';
import TagFilter from '../components/TagFilter';
import AddTodoForm from '../components/AddTodoForm';
import { Plus, Search, Filter, CheckCircle, Clock, Target } from 'lucide-react';

const TodoList: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTagId, setSelectedTagId] = useState<string>('');
  const [selectedPriority, setSelectedPriority] = useState<string>('');
  const [showCompleted, setShowCompleted] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  
  const { addNotification } = useNotification();

  useEffect(() => {
    fetchTodos();
    fetchTags();
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await todoApi.getTodos();
      setTodos(response.data);
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '할 일 목록을 불러오는데 실패했습니다',
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await tagApi.getTags();
      setTags(response.data);
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '태그 목록을 불러오는데 실패했습니다',
      });
    }
  };

  const handleAddTodo = async (todoData: { title: string; description?: string; tagId?: string; priority?: string }) => {
    try {
      const response = await todoApi.createTodo(todoData);
      setTodos(prev => [response.data, ...prev]);
      setShowAddForm(false);
      addNotification({
        type: 'success',
        message: '할 일이 성공적으로 추가되었습니다!',
      });
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '할 일 추가에 실패했습니다',
      });
    }
  };

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    try {
      const response = await todoApi.updateTodo(id, updates);
      setTodos(prev => prev.map(todo => 
        todo.id === id ? response.data : todo
      ));
      addNotification({
        type: 'success',
        message: '할 일이 성공적으로 수정되었습니다!',
      });
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '할 일 수정에 실패했습니다',
      });
    }
  };

  const handleDeleteTodo = async (id: string) => {
    if (!confirm('정말로 이 할 일을 삭제하시겠습니까?')) return;
    
    try {
      await todoApi.deleteTodo(id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
      addNotification({
        type: 'success',
        message: '할 일이 성공적으로 삭제되었습니다!',
      });
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '할 일 삭제에 실패했습니다',
      });
    }
  };

  const handleToggleComplete = async (id: string) => {
    try {
      const response = await todoApi.toggleComplete(id);
      setTodos(prev => prev.map(todo => 
        todo.id === id ? response.data : todo
      ));
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '할 일 상태 변경에 실패했습니다',
      });
    }
  };

  const filteredTodos = todos.filter(todo => {
    const matchesSearch = todo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         todo.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTag = !selectedTagId || todo.tagId === selectedTagId;
    const matchesPriority = !selectedPriority || todo.priority === selectedPriority;
    const matchesCompleted = showCompleted || !todo.completed;
    
    return matchesSearch && matchesTag && matchesPriority && matchesCompleted;
  });

  const completedCount = todos.filter(todo => todo.completed).length;
  const pendingCount = todos.filter(todo => !todo.completed).length;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">내 할 일</h1>
          <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600">
            <div className="flex items-center space-x-1">
              <Target className="h-4 w-4" />
              <span>전체 {todos.length}개</span>
            </div>
            <div className="flex items-center space-x-1">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <span>완료 {completedCount}개</span>
            </div>
            <div className="flex items-center space-x-1">
              <Clock className="h-4 w-4 text-orange-600" />
              <span>진행 중 {pendingCount}개</span>
            </div>
          </div>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors font-medium shadow-lg hover:shadow-xl"
        >
          <Plus className="h-5 w-5" />
          <span>할 일 추가</span>
        </button>
      </div>

      {/* Quick Stats */}
      {todos.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl p-4 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">전체 할 일</p>
                <p className="text-2xl font-bold">{todos.length}</p>
              </div>
              <Target className="h-8 w-8 text-blue-200" />
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-4 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100 text-sm">완료된 할 일</p>
                <p className="text-2xl font-bold">{completedCount}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-200" />
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-xl p-4 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100 text-sm">진행 중</p>
                <p className="text-2xl font-bold">{pendingCount}</p>
              </div>
              <Clock className="h-8 w-8 text-orange-200" />
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="할 일 검색..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <TagFilter
              tags={tags}
              selectedTagId={selectedTagId}
              onTagSelect={setSelectedTagId}
              onCreateTag={fetchTags}
            />
            
            <select
              value={selectedPriority}
              onChange={(e) => setSelectedPriority(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">모든 우선순위</option>
              <option value="low">낮음</option>
              <option value="medium">보통</option>
              <option value="high">높음</option>
            </select>
            
            <label className="flex items-center space-x-2 text-sm whitespace-nowrap">
              <input
                type="checkbox"
                checked={showCompleted}
                onChange={(e) => setShowCompleted(e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span>완료된 항목 표시</span>
            </label>
          </div>
        </div>
      </div>

      {/* Add Todo Form */}
      {showAddForm && (
        <AddTodoForm
          tags={tags}
          onSubmit={handleAddTodo}
          onCancel={() => setShowAddForm(false)}
        />
      )}

      {/* Todo List */}
      <div className="space-y-4">
        {filteredTodos.length > 0 ? (
          filteredTodos.map(todo => (
            <TodoItem
              key={todo.id}
              todo={todo}
              tags={tags}
              onUpdate={handleUpdateTodo}
              onDelete={handleDeleteTodo}
              onToggleComplete={handleToggleComplete}
            />
          ))
        ) : (
          <div className="text-center py-16">
            <div className="text-gray-400 text-6xl mb-4">📝</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              {searchTerm || selectedTagId || selectedPriority
                ? '검색 결과가 없습니다'
                : '아직 할 일이 없습니다'}
            </h3>
            <p className="text-gray-600 mb-6">
              {searchTerm || selectedTagId || selectedPriority
                ? '검색 조건을 변경하거나 새로운 할 일을 추가해보세요'
                : '첫 번째 할 일을 추가하여 시작해보세요'}
            </p>
            {!showAddForm && (
              <button
                onClick={() => setShowAddForm(true)}
                className="inline-flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors font-medium"
              >
                <Plus className="h-5 w-5" />
                <span>할 일 추가</span>
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TodoList;