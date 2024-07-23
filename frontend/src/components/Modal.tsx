import React from "react";

interface ModalProps {
  show: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ show, onClose, children }) => {
  if (!show) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-4 rounded shadow-lg">
        <div className="flex justify-center">
          <h2 className="flex-none text-center text-2xl font-bold mt-2 text-gray-900">
            Add New Project
          </h2>
          <button 
          className="flex-none justify-center rounded-md bg-red-500 px-3 ml-10 mt-3 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-red-400"
          onClick={onClose}>
            x Close
          </button>
        </div>
        {children}
      </div>
    </div>
  );
};

export default Modal;
