export type ToastKind = 'success' | 'error';

interface ToastProps {
  kind: ToastKind;
  message: string;
  onClose: () => void;
}

export function Toast({ kind, message, onClose }: ToastProps) {
  return (
    <div
      className={`fixed bottom-5 right-5 z-[60] rounded-xl px-4 py-3 text-sm font-semibold text-white shadow-lg ${
        kind === 'success' ? 'bg-emerald-600' : 'bg-rose-600'
      }`}
      role="status"
    >
      <button className="mr-3" onClick={onClose} aria-label="Dismiss notification">
        ×
      </button>
      {message}
    </div>
  );
}
