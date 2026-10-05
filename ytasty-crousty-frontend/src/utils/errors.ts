import axios from "axios";

export function getErrorMessage(error: unknown): string {
  if (typeof error === "string") return error;

  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return "Impossible de joindre le serveur";
    }

    const detail: unknown = (error.response.data as { detail?: unknown } | undefined)?.detail;
    if (typeof detail === "string") return detail;

    if (Array.isArray(detail)) {
      const first: unknown = detail[0];
      if (typeof first === "object" && first !== null && "msg" in first && typeof first.msg === "string") {
        return first.msg;
      }
    }

    return `Erreur ${error.response.status}`;
  }

  if (typeof error === "object" && error !== null && "message" in error && typeof error.message === "string") {
    return error.message;
  }

  return "Une erreur est survenue";
}