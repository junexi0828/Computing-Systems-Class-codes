import React, { useState, useEffect } from 'react';
import { useNotification } from '../context/NotificationContext';
import { todoApi } from '../services/api';
import { Statistics as StatsType } from '../types';
import { BarChart3, TrendingUp, CheckCircle, Clock, Target, Award, Calendar, Tag } from 'lucide-react';

const Statistics: React.FC = () => {
  const [stats, setStats] = useState<StatsType | null>(null);
  const [loading, setLoading] = useState(true);
  
  const { addNotification } = useNotification();

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      const response = await todoApi.getStatistics();
      setStats(response.data);
    } catch (error: any) {
      addNotification({
        type: 'error',
        message: '통계 데이터를 불러오는데 실패했습니다',
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="text-center py-16">
        <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-gray-900 mb-2">통계 데이터가 없습니다</h3>
        <p className="text-gray-600">할 일을 추가하면 통계를 확인할 수 있습니다</p>
      </div>
    );
  }

  const priorityColors = {
    low: { bg: 'bg-green-500', text: 'text-green-600', light: 'bg-green-100' },
    medium: { bg: 'bg-yellow-500', text: 'text-yellow-600', light: 'bg-yellow-100' },
    high: { bg: 'bg-red-500', text: 'text-red-600', light: 'bg-red-100' },
  };

  const priorityLabels = {
    low: '낮음',
    medium: '보통',
    high: '높음',
  };

  const maxTagCount = Math.max(...stats.tagDistribution.map(tag => tag.count), 1);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">📊 생산성 통계</h1>
        <p className="text-gray-600">할 일 관리 현황을 한눈에 확인해보세요</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">전체 할 일</p>
              <p className="text-3xl font-bold mt-1">{stats.total}</p>
            </div>
            <div className="p-3 bg-blue-400 bg-opacity-30 rounded-xl">
              <Target className="h-8 w-8" />
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">완료된 할 일</p>
              <p className="text-3xl font-bold mt-1">{stats.completed}</p>
            </div>
            <div className="p-3 bg-green-400 bg-opacity-30 rounded-xl">
              <CheckCircle className="h-8 w-8" />
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-100 text-sm font-medium">진행 중</p>
              <p className="text-3xl font-bold mt-1">{stats.pending}</p>
            </div>
            <div className="p-3 bg-orange-400 bg-opacity-30 rounded-xl">
              <Clock className="h-8 w-8" />
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm font-medium">완료율</p>
              <p className="text-3xl font-bold mt-1">{Math.round(stats.completionRate)}%</p>
            </div>
            <div className="p-3 bg-purple-400 bg-opacity-30 rounded-xl">
              <TrendingUp className="h-8 w-8" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Priority Distribution */}
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Award className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">우선순위별 분포</h3>
          </div>
          
          <div className="space-y-6">
            {Object.entries(stats.priorityDistribution).map(([priority, count]) => {
              const percentage = stats.total > 0 ? (count / stats.total) * 100 : 0;
              const config = priorityColors[priority as keyof typeof priorityColors];
              const label = priorityLabels[priority as keyof typeof priorityLabels];
              
              return (
                <div key={priority} className="space-y-3">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-3">
                      <div className={`w-4 h-4 rounded-full ${config.bg}`}></div>
                      <span className="font-semibold text-gray-900">{label}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-lg font-bold text-gray-900">{count}</span>
                      <span className="text-sm text-gray-500 ml-1">({Math.round(percentage)}%)</span>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${config.bg}`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Completion Overview */}
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">완료 현황</h3>
          </div>
          
          <div className="space-y-6">
            <div className="flex justify-center">
              <div className="relative w-40 h-40">
                <svg className="w-40 h-40 transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="2"
                  />
                  <path
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#10b981"
                    strokeWidth="2"
                    strokeDasharray={`${stats.completionRate}, 100`}
                    className="transition-all duration-700"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <span className="text-3xl font-bold text-gray-900">
                      {Math.round(stats.completionRate)}%
                    </span>
                    <p className="text-sm text-gray-500">완료율</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-6">
              <div className="text-center p-4 bg-green-50 rounded-xl">
                <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
                <p className="text-sm text-green-700 font-medium">완료됨</p>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-xl">
                <p className="text-2xl font-bold text-orange-600">{stats.pending}</p>
                <p className="text-sm text-orange-700 font-medium">진행 중</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tag Distribution */}
      {stats.tagDistribution.length > 0 && (
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Tag className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">태그별 할 일 분포</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {stats.tagDistribution.map((tag, index) => {
              const percentage = (tag.count / maxTagCount) * 100;
              const colors = [
                'bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-pink-500',
                'bg-indigo-500', 'bg-yellow-500', 'bg-red-500', 'bg-teal-500'
              ];
              const bgColor = colors[index % colors.length];
              
              return (
                <div key={tag.tagId} className="space-y-3">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-3">
                      <div className={`w-4 h-4 rounded-full ${bgColor}`}></div>
                      <span className="font-semibold text-gray-900">{tag.tagName}</span>
                    </div>
                    <span className="text-lg font-bold text-gray-900">{tag.count}개</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${bgColor}`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Motivational Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white text-center">
        <div className="max-w-2xl mx-auto">
          <h3 className="text-2xl font-bold mb-4">🎉 훌륭한 진전이에요!</h3>
          <p className="text-blue-100 text-lg mb-6">
            지금까지 {stats.completed}개의 할 일을 완료하셨습니다. 
            {stats.completionRate >= 70 
              ? ' 정말 대단한 성과입니다!' 
              : ' 조금만 더 힘내세요!'}
          </p>
          <div className="flex justify-center space-x-8">
            <div className="text-center">
              <p className="text-3xl font-bold">{stats.total}</p>
              <p className="text-blue-200">총 할 일</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold">{Math.round(stats.completionRate)}%</p>
              <p className="text-blue-200">완료율</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Statistics;