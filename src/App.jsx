import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import UploadPage from './pages/UploadPage';
import MeetingsPage from './pages/MeetingsPage';
import MeetingDetailPage from './pages/MeetingDetailPage';
import SearchPage from './pages/SearchPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-900">
                    AI Meeting Intelligence
                  </h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <NavLink
                    to="/"
                    className={({ isActive }) =>
                      isActive
                        ? 'border-indigo-500 text-gray-900 border-b-2 py-4 px-1 text-sm font-medium'
                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 border-b-2 py-4 px-1 text-sm font-medium'
                    }
                  >
                    Upload
                  </NavLink>
                  <NavLink
                    to="/meetings"
                    className={({ isActive }) =>
                      isActive
                        ? 'border-indigo-500 text-gray-900 border-b-2 py-4 px-1 text-sm font-medium'
                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 border-b-2 py-4 px-1 text-sm font-medium'
                    }
                  >
                    Meetings
                  </NavLink>
                  <NavLink
                    to="/search"
                    className={({ isActive }) =>
                      isActive
                        ? 'border-indigo-500 text-gray-900 border-b-2 py-4 px-1 text-sm font-medium'
                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 border-b-2 py-4 px-1 text-sm font-medium'
                    }
                  >
                    Search
                  </NavLink>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto py-6 px-4">
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/meetings" element={<MeetingsPage />} />
            <Route path="/meetings/:id" element={<MeetingDetailPage />} />
            <Route path="/search" element={<SearchPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;