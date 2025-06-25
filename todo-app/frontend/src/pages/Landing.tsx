import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import LoginModal from '../components/LoginModal';
import RegisterModal from '../components/RegisterModal';
import { CheckSquare, Target, BarChart3, Tag, Users, Zap, ArrowRight, Star } from 'lucide-react';

const Landing: React.FC = () => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const { user } = useAuth();
  const navigate = useNavigate();

  // 이미 로그인된 사용자는 todos 페이지로 리다이렉트
  React.useEffect(() => {
    if (user) {
      navigate('/todos');
    }
  }, [user, navigate]);

  const features = [
    {
      icon: Target,
      title: '스마트한 할 일 관리',
      description: '우선순위와 태그로 체계적으로 관리하세요'
    },
    {
      icon: BarChart3,
      title: '상세한 통계 분석',
      description: '완료율과 생산성을 한눈에 확인하세요'
    },
    {
      icon: Tag,
      title: '태그 기반 분류',
      description: '프로젝트별, 카테고리별로 정리하세요'
    },
    {
      icon: Zap,
      title: '빠른 접근성',
      description: '언제 어디서나 빠르게 접근 가능합니다'
    }
  ];

  const stats = [
    { number: '10K+', label: '활성 사용자' },
    { number: '50K+', label: '완료된 할 일' },
    { number: '99.9%', label: '서비스 안정성' },
    { number: '4.8★', label: '사용자 만족도' }
  ];

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <CheckSquare className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">TodoFlow</span>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowLoginModal(true)}
                className="text-gray-600 hover:text-blue-600 font-medium transition-colors"
              >
                로그인
              </button>
              <button
                onClick={() => setShowRegisterModal(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                시작하기
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-32">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              더 스마트한 방식으로
              <span className="block text-blue-600">할 일을 관리하세요</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              TodoFlow와 함께 생산성을 높이고, 목표를 달성하며, 성과를 추적하세요. 
              간단하지만 강력한 도구로 일상을 더욱 체계적으로 만들어보세요.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => setShowRegisterModal(true)}
                className="bg-blue-600 text-white px-8 py-4 rounded-xl hover:bg-blue-700 transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 flex items-center justify-center space-x-2"
              >
                <span>무료로 시작하기</span>
                <ArrowRight className="h-5 w-5" />
              </button>
              <button
                onClick={() => setShowLoginModal(true)}
                className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl hover:border-blue-600 hover:text-blue-600 transition-all duration-200 font-semibold text-lg"
              >
                로그인
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              왜 TodoFlow를 선택해야 할까요?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              단순한 할 일 목록을 넘어서, 생산성을 극대화하는 스마트한 기능들을 제공합니다.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="text-center p-6 rounded-2xl bg-gradient-to-br from-gray-50 to-blue-50 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-2"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 text-white rounded-2xl mb-4">
                  <feature.icon className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              신뢰받는 서비스
            </h2>
            <p className="text-xl text-blue-100 max-w-2xl mx-auto">
              전 세계 사용자들이 선택한 TodoFlow의 성과를 확인해보세요.
            </p>
          </div>
          
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl lg:text-5xl font-bold text-white mb-2">{stat.number}</div>
                <div className="text-blue-100 text-lg">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">
            지금 바로 시작해보세요
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            몇 분 안에 설정을 완료하고 더 나은 생산성을 경험해보세요.
          </p>
          <button
            onClick={() => setShowRegisterModal(true)}
            className="bg-blue-600 text-white px-8 py-4 rounded-xl hover:bg-blue-700 transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 inline-flex items-center space-x-2"
          >
            <span>무료 계정 만들기</span>
            <ArrowRight className="h-5 w-5" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <CheckSquare className="h-8 w-8 text-blue-400" />
              <span className="text-xl font-bold">TodoFlow</span>
            </div>
            <div className="text-gray-400">
              © 2025 TodoFlow. 모든 권리 보유.
            </div>
          </div>
        </div>
      </footer>

      {/* Modals */}
      <LoginModal 
        isOpen={showLoginModal} 
        onClose={() => setShowLoginModal(false)}
        onSwitchToRegister={() => {
          setShowLoginModal(false);
          setShowRegisterModal(true);
        }}
      />
      <RegisterModal 
        isOpen={showRegisterModal} 
        onClose={() => setShowRegisterModal(false)}
        onSwitchToLogin={() => {
          setShowRegisterModal(false);
          setShowLoginModal(true);
        }}
      />
    </div>
  );
};

export default Landing;