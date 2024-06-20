import React from 'react';

const HeaderComponent: React.FC = () => {
  return (
    <>
        <nav className="bg-gray-800">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              <div className="flex h-16 items-center justify-between">
                  <div className="flex items-center">
                      <div className="flex-shrink-0">
                          <img className="h-8 w-8" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500" alt="Your Company"/></div>
                      <div className="hidden md:block">
                          <div className="ml-10 flex items-baseline space-x-4">
                              <a href="#" className="rounded-md bg-gray-900 px-3 py-2 text-sm font-medium text-white" aria-current="page">Projects</a>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </nav>
      <header className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">Projects</h1>
        </div>
    </header></>
  );
};

export default HeaderComponent;