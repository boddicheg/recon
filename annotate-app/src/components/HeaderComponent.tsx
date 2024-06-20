import React from 'react';

const HeaderComponent: React.FC = () => {
  return (
    <header className="bg-blue-600 p-4 text-white shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">Annotate</h1>
        <nav>
          <ul className="flex space-x-4">
            <li><a href="/" className="hover:underline">Home</a></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default HeaderComponent;