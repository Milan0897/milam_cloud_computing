import { useEffect, useState } from 'react';

const toasts = [];
let toastId = 0;

export function useToast() {
  const [, setRender] = useState(0);

  const addToast = (message, type = 'success') => {
    const id = ++toastId;
    toasts.push({ id, message, type });
    setRender((n) => n + 1);
    setTimeout(() => removeToast(id), 4000);
  };

  const removeToast = (id) => {
    const index = toasts.findIndex((t) => t.id === id);
    if (index !== -1) {
      toasts.splice(index, 1);
      setRender((n) => n + 1);
    }
  };

  return { toasts: [...toasts], addToast, removeToast };
}

export function ToastContainer() {
  const { toasts, removeToast } = useToast();

  if (toasts.length === 0) return null;

  return (
    <div>
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`toast toast-${toast.type}`}
          onClick={() => removeToast(toast.id)}
        >
          {toast.message}
        </div>
      ))}
    </div>
  );
}