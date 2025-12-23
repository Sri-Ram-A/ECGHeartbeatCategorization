type Notifier = (opts: { type: "success" | "error" | "warn"; message: string }) => void;

let notifier: Notifier | null = null;

export function setNotifier(n: Notifier) {
  notifier = n;
}

export function clearNotifier() {
  notifier = null;
}

export function notifySuccess(message: string) {
  notifier?.({ type: "success", message });
}

export function notifyError(message: string) {
  notifier?.({ type: "error", message });
}

export function notifyWarn(message: string) {
  notifier?.({ type: "warn", message });
}

export default {
  setNotifier,
  clearNotifier,
  notifySuccess,
  notifyError,
  notifyWarn,
};
